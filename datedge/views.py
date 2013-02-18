from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datedge.models import Sitting, Question, Answer, Scaling, Activation
from datetime import date

def account_activate(request, user_id=None):
    today = date.today()
    expiry = date(today.year + 1, today.month, today.day)
    if not user_id:
        activation = Activation(user=request.user, expiry=expiry)
        activation.save()
    # else check admin and activate user
    return HttpResponse("account_activate")

def sitting_results(request, sitting_id):
    sitting = get_object_or_404(Sitting, pk=sitting_id)
    return render(request, 'results.html', {'sitting': sitting})

def sitting_new(request, test_id, is_timed=False):
    #check logged in and has activation
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    if not request.user.activation_set.filter(expiry__gte=date.today()):
        # set error message: please purchase access credits
        return HttpResponseRedirect('/purchase/')
    # check if no active sitting exists
    try:
        sitting = Sitting.objects.get(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
    except Sitting.DoesNotExist:
        sitting = Sitting(user=request.user, test_id=test_id, is_active=True, is_timed=is_timed)
        sitting.save()
    question = sitting.test.question_set.all()[0]
    return render(request, 'sitting.html', {'sitting': sitting, 'question': question})

def sitting_question(request, sitting_id, question_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    question = sitting.test.question_set.all()[int(question_id)-1]
    question.text = getattr(sitting.test, 'text' + str(question.text_idx))
    return render(request, 'question.html', {'sitting': sitting, 'question': question})

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

def sitting_review(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    return render(request, 'review.html', {'sitting': sitting})

def sitting_results(request, sitting_id):
    sitting = Sitting.objects.get(id=sitting_id, user=request.user)
    return render(request, 'results.html', {'sitting': sitting})
