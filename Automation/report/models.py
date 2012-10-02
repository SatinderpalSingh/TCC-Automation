from django.db import models
from django.forms import ModelForm, TextInput, ModelChoiceField
import datetime
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Max ,Q, Sum
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from Automation.tcc.models import ClientJob

################################
#Input data model for SOIL OSHR#
################################

class soil_ohsr(models.Model):
	Date_of_testing = models.CharField(max_length=255)
	Type_of_str = models.CharField(max_length=255)
	Latitude_N = models.CharField(max_length=255,blank=True)
	Longitude_E = models.CharField(max_length=255,blank=True)
	Presence_1 = models.CharField(max_length=255)
	Presence_2 = models.CharField(max_length=255,blank=True)
	Submitted_1 = models.CharField(max_length=255)
	Submitted_2 = models.CharField(max_length=255,blank=True)
	Submitted_3 = models.CharField(max_length=255,blank=True)
	Site_name = models.CharField(max_length=255)
	Water_table = models.CharField(max_length=255)
	Depth_D = models.CharField(max_length=255,blank=True)
	Diameter_B = models.CharField(max_length=255)
	Gama_G = models.CharField(max_length=255)
	C = models.CharField(max_length=255)
	Phay = models.CharField(max_length=255)	
	Phay_fe = models.CharField(max_length=255)
	Nc = models.CharField(max_length=255)
	Nq = models.CharField(max_length=255)
	Ny = models.CharField(max_length=255)
	dc = models.CharField(max_length=255)
	dqdy = models.CharField(max_length=255)
	Water = models.CharField(max_length=255)
	Pulse_Pulse = models.CharField(max_length=255)
	Eq_Total = models.CharField(max_length=255)
	Total_Dby_2 = models.CharField(max_length=255)
	Dt_1 = models.CharField(max_length=255)
	Dt_2 = models.CharField(max_length=255)
	Dt_3 = models.CharField(max_length=255)
	Dt_4 = models.CharField(max_length=255)
	Dt_5 = models.CharField(max_length=255)
	Dt_6 = models.CharField(max_length=255)
	Dt_7 = models.CharField(max_length=255)
	Dt_8 = models.CharField(max_length=255)
	Ob_Pr_1 = models.CharField(max_length=255)
	Ob_Pr_2 = models.CharField(max_length=255)
	Ob_Pr_3 = models.CharField(max_length=255)
	Ob_Pr_4 = models.CharField(max_length=255)
	Ob_Pr_5 = models.CharField(max_length=255)
	Ob_Pr_6 = models.CharField(max_length=255)
	Ob_Pr_7 = models.CharField(max_length=255)
	Ob_Pr_8 = models.CharField(max_length=255)
	Corr_F_1 = models.CharField(max_length=255)
	Corr_F_2 = models.CharField(max_length=255)
	Corr_F_3 = models.CharField(max_length=255)
	Corr_F_4 = models.CharField(max_length=255)
	Corr_F_5 = models.CharField(max_length=255)
	Corr_F_6 = models.CharField(max_length=255)
	Corr_F_7 = models.CharField(max_length=255)
	Corr_F_8 = models.CharField(max_length=255)
	Ob_N_V1 = models.CharField(max_length=255)
	Ob_N_V2 = models.CharField(max_length=255)
	Ob_N_V3 = models.CharField(max_length=255)
	Ob_N_V4 = models.CharField(max_length=255)
	Ob_N_V5 = models.CharField(max_length=255)
	Ob_N_V6 = models.CharField(max_length=255)
	Ob_N_V7 = models.CharField(max_length=255)
	Ob_N_V8 = models.CharField(max_length=255)
	Corr_N_V1 = models.CharField(max_length=255)
	Corr_N_V2 = models.CharField(max_length=255)
	Corr_N_V3 = models.CharField(max_length=255)
	Corr_N_V4 = models.CharField(max_length=255)
	Corr_N_V5 = models.CharField(max_length=255)
	Corr_N_V6 = models.CharField(max_length=255)
	Corr_N_V7 = models.CharField(max_length=255)
	Corr_N_V8 = models.CharField(max_length=255)
	N_Value = models.CharField(max_length=255)
	S = models.CharField(max_length=255)
	Value = models.CharField(max_length=255)
	Net_Value = models.CharField(max_length=255)
	
#	def __str__(self):
#		return self.date_of_testing

class soil_ohsrForm(ModelForm):
	class Meta :
		model = soil_ohsr
'''
class soil(models.Model):
    type_of_data = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    )
    year_in_school = models.CharField(max_length=2, choices=type_of_data)

class soilForm(ModelForm):
	class Meta :
		model = soil

'''
###################################
#header file for different reports#
###################################
class head(models.Model):
    job_no = models.ForeignKey(ClientJob)
    refrence_no = models.CharField(max_length=255)    			#college reference letter no. 
    dispatch_report_date = models.CharField(max_length=255)		#report dispatch date, to the client
    date_of_testing = models.CharField(max_length=255)			#date on which test is performed	
    subject = models.CharField(max_length=255)				
    reference = models.CharField(max_length=255)			#client reference letter no.
    column_1 = models.CharField(max_length=255,blank=True)
    column_2 = models.CharField(max_length=255,blank=True)
    column_3 = models.CharField(max_length=255,blank=True)
    
    def __str__(self):
        return self.subject
        
class headForm(ModelForm):
    class Meta :
        model = head
        
##############################
#report type cheical_analysis#        
##############################        
class chem_analysis(models.Model):
    job_no = models.ForeignKey(ClientJob)
    s_no = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
#    headers = models.ForeignKey(head)
    
    def __str__(self):
        return self.s_no
        
class chem_analysisForm(ModelForm):
    class Meta :
        model = chem_analysis
        
                        
