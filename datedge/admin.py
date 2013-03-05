from django.contrib import admin
from datedge.models import Sitting, Test, Question, Activation, Answer, Scaling, UserProfile

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Activation)
admin.site.register(Scaling)
admin.site.register(Sitting)
admin.site.register(Answer)
admin.site.register(UserProfile)
