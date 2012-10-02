from django.conf.urls.defaults import *
from django.contrib import admin
#from Automation.report.models import *

urlpatterns = patterns('Automation.report.views',
	#(r'^$', 'report_app'),
	(r'^report_pdf/$', 'report_pdf'),
	(r'^soil_ohsr/$', 'soil_ohsr'),
	#(r'^get_report/$', 'report_show'),
	(r'^report/$', 'report'),
	(r'^chemical_analysis/$', 'chemical_analysis'),
	(r'^header/$', 'header'),
	(r'^result/$', 'result'),
)

