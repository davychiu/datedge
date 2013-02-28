from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from datedge import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'datedge.views.home', name='home'),
    # url(r'^datedge/', include('datedge.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^home/$', views.home, name='home'),
    url(r'^refund/$', TemplateView.as_view(template_name='refund.html'), name='refund'),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    url(r'^terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    url(r'^trial/$', views.trial, name='trial'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^process/$', views.process, name='process'),
    url(r'^success/$', views.success, name='success'),
    url(r'^sitting/new/(?P<test_id>\d+)/timed/$', views.sitting_new, {'is_timed': True}),
    url(r'^sitting/new/(?P<test_id>\d+)/$', views.sitting_new, name='sitting_new'),
    url(r'^sitting/(?P<sitting_id>\d+)/question/(?P<question_id>\d+)/$', views.sitting_question, name='sitting_question'),
    url(r'^sitting/(?P<sitting_id>\d+)/question/(?P<question_id>\d+)/mark/$', views.sitting_mark),
    url(r'^sitting/(?P<sitting_id>\d+)/review/$', views.sitting_review),
    url(r'^sitting/(?P<sitting_id>\d+)/results/$', views.sitting_results, name='results'),
    url(r'^sitting/(?P<sitting_id>\d+)/end/$', views.sitting_end, name='sitting_end'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/activate/$', views.account_activate),
    url(r'^accounts/activate/(?P<user_id>\d+)/$', views.account_activate),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)

#monkey patch for django admin static files on heroku
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
