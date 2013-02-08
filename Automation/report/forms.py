from Automation.report.models import * # Change as necessary
#from Automation.tcc.models import *
from django.forms import ModelForm
'''
##################################
# From the module "TCC & Report" #
##################################
class headForm(ModelForm):
    	class Meta :
        	model = head
		exclude = ('material')
'''
#################################
# From the module "Report" only #
#################################
'''
class SearchForm(ModelForm):
    	class Meta :
        	model = Search
fields = ['job', 'report','material',]
'''
class ReportForm(ModelForm):
  	class Meta:
    		model = Report
    		exclude = ('job_id')

class CubeForm(ModelForm):
	class Meta:
		model = Cube
    		exclude = ('Report_id','ip_address')

class Chem_analysisForm(ModelForm):
	class Meta :
		model = Chem_analysis
		exclude = ('Report_id','ip_address')
 
class SteelForm(ModelForm):
	class Meta :
		model = Steel
		exclude = ('Report_id','ip_address')

class Ground_WaterForm(ModelForm):
	class Meta :
		model = Ground_Water
		exclude = ('Report_id','ip_address')

class Concrete_PaverForm(ModelForm):
	class Meta :
		model = Concrete_Paver
		exclude = ('Report_id','ip_address')
 
class PCForm(ModelForm):
	class Meta :
		model = PC
		exclude = ('Report_id','ip_address')

class Rebound_Hammer_TestingForm(ModelForm):
	class Meta :
		model = Rebound_Hammer_Testing
		exclude = ('Report_id','ip_address')

class BrickForm(ModelForm):
	class Meta :
		model = Brick
		exclude = ('Report_id','ip_address')

class WaterForm(ModelForm):
	class Meta :
		model = Water
		exclude = ('Report_id','ip_address')

class Soil_OhsrForm(ModelForm):
	class Meta :
		model = Soil_Ohsr
		exclude = ('Report_id','ip_address')		

class Soil_BuildingForm(ModelForm):
	class Meta :
		model = Soil_Building
		exclude = ('Report_id','ip_address')		

class AdmixtureForm(ModelForm):
	class Meta :
		model = Admixture
		exclude = ('Report_id','ip_address')		

class Cement_PPCForm(ModelForm):
	class Meta :
		model = Cement_PPC
		exclude = ('Report_id','ip_address')		

class Cement_OPC_33Form(ModelForm):
	class Meta :
		model = Cement_OPC_33
		exclude = ('Report_id','ip_address')		

class Cement_OPC_43Form(ModelForm):
	class Meta :
		model = Cement_OPC_43
		exclude = ('Report_id','ip_address')		

class Cement_OPC_53Form(ModelForm):
	class Meta :
		model = Cement_OPC_53
		exclude = ('Report_id','ip_address')		



