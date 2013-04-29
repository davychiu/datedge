from django.contrib import admin
from datedge.models import Sitting, Test, Question, Activation, Answer, Scaling, UserProfile

class SittingAdmin(admin.ModelAdmin):
    list_display = ('id','test_id','is_active','user','score_percent','created_date','modified_date')

    def test_id(self, instance):
        return instance.test.id if instance.test.id is not 6 else 'trial'

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Activation)
admin.site.register(Scaling)
admin.site.register(Sitting, SittingAdmin)
admin.site.register(Answer)
admin.site.register(UserProfile)
