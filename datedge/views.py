from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datedge.models import Sitting, Question, Answer, Scaling

#def question_answer(request):
    
#def question_mark(request):

def sitting_results(request, sitting_id):
    sitting = get_object_or_404(Sitting, pk=sitting_id)
    return render(request, 'results.html', {'sitting': sitting})

def sitting_new(request, test_id, is_timed=False):
    sitting = Sitting(user_id=1,test_id=test_id,is_active=True,is_timed=is_timed)
    question = sitting.test.question_set.all()[0]
    return render(request, 'sitting.html', {'sitting': sitting, 'question': question})

#def user_activate():

