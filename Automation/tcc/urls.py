from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from Automation.tcc.models import *


urlpatterns = patterns('Automation.tcc.views',
    (r'^report_header/$', 'report_header'),
    (r'^index/$', 'index1'),
    (r'^catalog/$', 'catalog'),
    (r'^previous/$', 'previous'),
    (r'^addprofile/$', 'profile'),
    (r'^performa/$', 'performa'),
    (r'^field/$', 'field'),
    (r'^rate/$', 'rate'),
    (r'^performa/$', 'performa'),
    (r'^add_job/$', 'field_test_select'),
    (r'^test-by-material-id/$', 'field_test_select'),
    #(r'^test-by-material-id/(\d+)/$', 'feed_test'),
    #(r'^prev/$',''),
    (r'^tests/$', 'tests',),
    (r'^field/(?P<field>[-\w]+)/all_json_tests/$', 'all_json_tests'),
   
)

