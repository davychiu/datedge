from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datedge.models import Sitting, Question, Answer, Scaling, Activation, Test
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from datedge.helpers import activation_required
import stripe

@login_required
def home(request):
    test_data = []
    tests = Test.objects.exclude(id=6)
    for test in tests:
        test_data.append({'test': test, 'sittings': request.user.sitting_set.filter(test=test)})
    return render(request, 'home.html', {'test_data': test_data})

def account_activate(request, user_id=None):
    today = date.today()
    expiry = date(today.year + 1, today.month, today.day)
    if not user_id:
        activation = Activation(user=request.user, expiry=expiry)
        activation.save()
    # else check admin and activate user
    return HttpResponse("account_activate")

@login_required
def account_home(request):
    return HttpResponse("account_home")

@login_required
def trial(request):
    test_id = 6
    is_timed = True
    # check if no active sitting exists
    try:
        sitting = Sitting.objects.get(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
    except Sitting.DoesNotExist:
        sitting = Sitting(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
        sitting.save()
    question = sitting.test.question_set.all()[0]
    return render(request, 'sitting.html', {'sitting': sitting, 'question': question})

@login_required
def sitting_results(request, sitting_id):
    sitting = get_object_or_404(Sitting, pk=sitting_id)
    return render(request, 'results.html', {'sitting': sitting})

@login_required
@user_passes_test(activation_required, '/purchase/')
def sitting_new(request, test_id, is_timed=False):
    # check if no active sitting exists
    try:
        sitting = Sitting.objects.get(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
    except Sitting.DoesNotExist:
        sitting = Sitting(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
        sitting.save()
    question = sitting.test.question_set.all()[0]
    return render(request, 'sitting.html', {'sitting': sitting, 'question': question})

@login_required
def sitting_question(request, sitting_id, question_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    question = sitting.test.question_set.all()[int(question_id)-1]
    question.text = getattr(sitting.test, 'text' + str(question.text_idx))
    return render(request, 'question.html', {'sitting': sitting, 'question': question})

@login_required
@user_passes_test(activation_required, '/purchase/')
def sitting_mark(request, sitting_id, question_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    question = sitting.test.question_set.all()[int(question_id)-1]
    # check if no answer exists
    try:
        answer = sitting.answer_set.filter(question_id=question_id)[0]
        answer.is_marked = not answer.is_marked
        answer.save()
    except Answer.DoesNotExist:
        answer = Answer(user=request.user, sitting=sitting, question_id=question_id, is_marked=True)
        answer.save()
    return render(request, 'question.html', {'sitting': sitting, 'question': question})

@login_required
def sitting_review(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    question_data = []
    for question in sitting.test.question_set.all():
        marked = True if question in sitting.test.question_set.filter(answer__is_marked=True, answer__sitting=sitting) else False
        completed = True if question in sitting.test.question_set.exclude(answer__answer_idx=None, answer__sitting=sitting) else False
        skipped = True if question in sitting.test.question_set.filter(answer__answer_idx=None, answer__sitting=sitting) else False
        question_data.append({'question': question, 
                            'marked': marked, 
                            'completed': completed,
                            'skipped': skipped})
    return render(request, 'review.html', {'sitting': sitting, 'question_data': question_data})

@login_required
def sitting_results(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    return render(request, 'results.html', {'sitting': sitting})

@login_required
@user_passes_test(activation_required, '/purchase/')
def sitting_end(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    sitting.is_active = False
    sitting.save()
    return HttpResponse('sitting_end')

def purchase(request):
    return HttpResponse('purchase')

def checkout(request):
    from django.conf import settings
    return render(request, 'checkout.html', {'STRIPE_PUBLISHABLE': settings.STRIPE_PUBLISHABLE})

def process(request):
    from django.conf import settings
    # set your secret key: remember to change this to your live secret key in production
    # see your keys here https://manage.stripe.com/account
    stripe.api_key = settings.STRIPE_SECRET

    # get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # create the charge on Stripe's servers - this will charge the user's card
    charge = stripe.Charge.create(
        amount=6500, # amount in cents, again
        currency="cad",
        card=token,
        description="DATEdge: " + request.user.email
    )
    return success(request) #HttpResponse('purchase sucess')

def success(request):
    return HttpResponse('success')
