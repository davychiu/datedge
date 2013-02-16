from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
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
    url(r'^sitting/new/(?P<test_id>\d+)/timed/$', views.sitting_new, {'is_timed': True}),
    url(r'^sitting/new/(?P<test_id>\d+)/$', views.sitting_new, name='new'),
    url(r'^sitting/(?P<sitting_id>\d+)/results/$', views.sitting_results, name='results'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)
