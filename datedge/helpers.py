from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datedge.models import Sitting
from functools import wraps
from django.utils.decorators import available_attrs

def activation_required(view_func):   
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        sitting_id = kwargs.get('sitting_id', None)
        sitting = Sitting.objects.get(id=sitting_id) if sitting_id else None
        test_id = sitting.test.id if sitting else kwargs.get('test_id', None)
        if request.user.get_profile().is_activated or int(test_id) is 6:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('purchase'))
    return wrapper

def valid_sitting_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        sitting_id = kwargs.get('sitting_id', None)
        sitting = Sitting.objects.get(id=sitting_id) if sitting_id else None
        if sitting.is_timed and (datetime.utcnow() - sitting.created_date.replace(tzinfo=None)).seconds >= 3600:
            sitting.is_active = False
            sitting.save()
        return view_func(request, *args, **kwargs)
    return wrapper    
