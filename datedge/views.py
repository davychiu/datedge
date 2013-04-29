from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datedge.models import Sitting, Question, Answer, Scaling, Activation, Test
from datedge.forms import QuestionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from datedge.helpers import activation_required, valid_sitting_required
from datedge import settings
from django.core.mail import send_mail
import stripe

def main(request):
    meta_description = "Get Instant Access To DAT Edge Practice Exams. Sign Up Now To Get A Free Sample Test!"
    return render(request, 'base.html', {'STATIC_URL': settings.STATIC_URL, 'META_DESCRIPTION': meta_description})

@login_required
def home(request):
    test_data = []
    sittings = Sitting.objects.filter(user=request.user, is_active=True)
    if sittings:
        sittings.update(is_active=False)
    tests = Test.objects.exclude(id=6)
    sample_test = Test.objects.get(id=6)
    test_data.append({'test': sample_test, 'sittings': request.user.sitting_set.filter(test=sample_test)[:5]})
    expiry = request.user.activation_set.filter(expiry__gte=date.today())[0].expiry if request.user.get_profile().is_activated else None
    for test in tests:
        test_data.append({'test': test, 'sittings': request.user.sitting_set.prefetch_related('test').filter(test=test)[:5]})
    return render(request, 'home.html', {'test_data': test_data, 'expiry': expiry})

def account_activate(request, user_id=None):
    today = date.today()
    expiry = date(today.year, today.month + 6, today.day)
    if not user_id:
        activation = Activation(user=request.user, expiry=expiry)
        activation.save()
    # else check admin and activate user
    return HttpResponse("account_activate")

@login_required
def trial(request):
    test_id = 6
    return render(request, 'sitting.html', {'test_id': test_id})

@login_required
@activation_required
@valid_sitting_required
def sitting_results(request, sitting_id):
    sitting = get_object_or_404(Sitting, pk=sitting_id)
    return render(request, 'results.html', {'sitting': sitting})

@login_required
@activation_required
def sitting_stage(request, test_id):
    return render(request, 'sitting.html', {'test_id': test_id})

@login_required
@activation_required
def sitting_new(request, test_id, is_timed=False):
    # check if no active sitting exists
    sitting = Sitting(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
    sitting.save()
    return HttpResponseRedirect(reverse('sitting_question', kwargs={'sitting_id': sitting.id, 'question_id': 1}))

@login_required
@activation_required
def sitting_question(request, sitting_id, question_id, review_marked=False, review_incomplete=False):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user) 
# snippet to generate review checks and exes
    questions = []
    for question in sitting.test.question_set.all():
        try:
            answer = sitting.answer_set.get(question=question)
        except Answer.DoesNotExist:
            answer = None
        question.is_correct = False
        if answer:
            if question.answer_idx is answer.answer_idx:
                question.is_correct = True
        questions.append({'question': question})

    question_set = ''
    post_redirect = ''
    if review_marked:
        question_set = sitting.marked
        post_redirect = 'sitting_review_marked'
    elif review_incomplete:
        question_set = sitting.incomplete
        post_redirect = 'sitting_review_incomplete'
    else:
        question_set = sitting.test.question_set.all()
        post_redirect = 'sitting_question'
    question = question_set[int(question_id)-1]        
    try:
        answer = Answer.objects.get(sitting=sitting, question=question, user=request.user) 
    except Answer.DoesNotExist:
        answer = None
    try:
        question.back = question_set[int(question_id)-1] if int(question_id) > 1 else None
        question.next = question_set[int(question_id)] if int(question_id) < question_set.count() else None
    except IndexError:
        question.next = question.back = None
    question.text = getattr(sitting.test, 'text' + str(question.text_idx))
    options = [getattr(question, 'option' + str(idx)) for idx in range(1,6)]
    if request.POST:
        form = QuestionForm(request.POST, options=options)
        is_mark = True if "submit_mark" in request.POST else False
        if form.is_valid():
            #save answer
            if sitting.is_active:
                answer_idx = form.cleaned_data['answer'] or None
                if not answer:
                    answer = Answer(sitting=sitting, question=question, user=request.user, answer_idx=answer_idx)
                if answer.answer_idx is not answer_idx:
                    answer.answer_idx = answer_idx
                if is_mark:
                    answer.is_marked = not answer.is_marked
                answer.save()
            #return next/prev question
            is_forward = True if "submit_next" in request.POST else False
            #for marked and incomplete, check if set has shrunk and reset question_id
            if review_marked:
                question_set = sitting.marked
            elif review_incomplete:
                question_set = sitting.incomplete
            if review_marked or review_incomplete:
                if question not in question_set:
                    question_id = str(int(question_id)-1)
                    is_forward = True
                    is_mark = False
            offset = 1 if is_forward else -1
            offset = 0 if is_mark else offset
            if int(question_id) >= question_set.count() and offset == 1:
                return HttpResponseRedirect(reverse('sitting_review', kwargs={'sitting_id': sitting_id}))
            else:
                return HttpResponseRedirect(reverse(post_redirect, kwargs={'sitting_id': sitting_id, 'question_id': str(int(question_id) + offset), 'review_marked': review_marked, 'review_incomplete': review_incomplete}))
        else:
            return HttpResponse(str(form.errors)) 
    else:
        answer_idx = answer.answer_idx if hasattr(answer, 'answer_idx') else None
        form = QuestionForm(options=options, active=sitting.is_active, initial={'answer': answer_idx}, auto_id=False)
        question.num = list(sitting.test.question_set.all().values_list('id', flat=True)).index(int(question.id)) + 1
        question.is_marked = answer.is_marked if hasattr(answer, 'is_marked') else None
        return render(request, 'question.html', {'sitting': sitting, 'question': question, 'form':form, 'questions':questions})

@login_required
@activation_required
def sitting_mark(request, sitting_id, question_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    question = sitting.test.question_set.all()[int(question_id)-1]
    options = [getattr(question, 'option' + str(idx)) for idx in range(1,6)]
    form = QuestionForm(request.POST, options=options)
    if sitting.is_active and form.is_valid():
        # check if no answer exists
        answer_idx = form.cleaned_data['answer'] or None
        try:
            answer = sitting.answer_set.get(question=question.id)
            answer.is_marked = not answer.is_marked
            answer.answer_idx = answer_idx
            answer.save()
        except Answer.DoesNotExist:
            answer = Answer(user=request.user, sitting=sitting, question_id=question.id, is_marked=True, answer_idx=answer_idx)
            answer.save()
    return HttpResponseRedirect(reverse('sitting_question', kwargs={'sitting_id': sitting_id, 'question_id': question_id}))

@login_required
@activation_required
def sitting_review(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    sitting.incomplete_count = sitting.test.question_set.count() - sitting.complete.count()
    question_data = []
    for question in sitting.test.question_set.all():
        marked = True if question in sitting.test.question_set.filter(answer__is_marked=True, answer__sitting=sitting) else False
        completed = True if question in sitting.test.question_set.filter(answer__answer_idx__isnull=False, answer__sitting=sitting, answer__question=question) else False
        skipped = True if question in sitting.test.question_set.filter(answer__answer_idx=None, answer__sitting=sitting) else False
        question_data.append({'question': question, 
                            'marked': marked, 
                            'completed': completed,
                            'skipped': skipped})
    return render(request, 'review.html', {'sitting': sitting, 'question_data': question_data})

@login_required
@activation_required
def sitting_results(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    questions = []
    for question in sitting.test.question_set.all():
        try:
            answer = sitting.answer_set.get(question=question)
        except Answer.DoesNotExist:
            answer = None
        question.is_correct = False
        if answer:
            if question.answer_idx is answer.answer_idx:
                question.is_correct = True
        questions.append({'question': question})
    return render(request, 'results.html', {'sitting': sitting, 'questions': questions})

@login_required
@activation_required
def sitting_end(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    if sitting.is_active:
        sitting.is_active = False
        sitting.save()
    return HttpResponseRedirect(reverse('sitting_results', kwargs={'sitting_id': sitting_id}))

@login_required
def purchase(request):
    from django.conf import settings
    return render(request, 'checkout.html', {'STRIPE_PUBLISHABLE': settings.STRIPE_PUBLISHABLE})

@login_required
def process(request):
    from django.conf import settings
    # set your secret key: remember to change this to your live secret key in production
    # see your keys here https://manage.stripe.com/account
    stripe.api_key = settings.STRIPE_SECRET

    # get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # create the charge on Stripe's servers - this will charge the user's card
    charge = stripe.Charge.create(
        amount=4900, # amount in cents, again
        currency="usd",
        card=token,
        description="DAT Edge: " + request.user.email
    )
    today = date.today()
    [exp_y, exp_m] = divmod(today.month + 6, 12)
    expiry = date(today.year + exp_y, exp_m, today.day)
    activation = Activation(user=request.user, expiry=expiry)
    activation.save()

    return success(request) #HttpResponse('purchase sucess')

@login_required
def success(request):
    send_mail('DAT Edge Purchase', 'Thank you for purchasing the DAT Edge Reading Comprehension Practice Tests.\n\n====================\nYour Login Details\n====================\n\nUsername: ' + request.user.username + '\n\nLogin to start taking the practice tests: http://www.datedge.com/accounts/login/\n\nIf you have any questions, please email us at support@datedge.com\n\nRegards,\nThe DAT Edge Team\nwww.datedge.com','support@datedge.com',[request.user.email])
    send_mail('DAT Edge Purchase: ' + request.user.username,'','support@datedge.com',['davychiu@gmail.com', 'umuhamm@gmail.com'])
    return render(request, 'success.html')
