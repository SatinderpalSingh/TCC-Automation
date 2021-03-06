"""
Automation Model Module
 
This contains all of the definitions for the model of the Testing & Consultancy Cell Automation,
including the tables, classes and mappers.
 
"""

from django.db import models
from django.forms import ModelForm, TextInput, ModelChoiceField
import datetime
from django import forms
#from django.utils.translation import ugettext as _
from Automation.tcc.choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Max ,Q, Sum
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
#from tagging.fields import TagField
from Automation.report.models import *
#from smart_selects.db_fields import ChainedForeignKey

class Report(models.Model):
	"""
	Define Client Report Form to reterive any Report Information,
	when we fill Job Number and type of Report Store in Database
	"""
	id = models.IntegerField(primary_key=True)
	type_of_report = models.CharField(max_length=50)

class UserProfile(models.Model):
    # This field is required.
        user = models.OneToOneField(User)

    # Other fields here
        name = models.CharField(max_length=255,)
	address_1 =models.CharField(max_length=255 ,blank=True )
	address_2 =models.CharField(max_length=255, blank=True )
	city =models.CharField(max_length=255,blank=True)
	pin_code = models.IntegerField(null=True)
	state=models.CharField(max_length=30, blank = True,choices=STATES_CHOICES)
	website =models.URLField(blank=True)
	contact_no =models.CharField(max_length=25,blank=True)
	type_of_organisation = models.CharField(max_length=20,choices=ORGANISATION_CHOICES)

	def __unicode__(self):
        	return self.name


class UserProfileForm(ModelForm):
	class Meta :
		model = UserProfile	
		widgets = {
            'name': TextInput(attrs={'size': 30}),
            'address_1': TextInput(attrs={'size': 30}),
            'address_1': TextInput(attrs={'size': 30}),
			}

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
 

class Auto_number(models.Model):
	id = models.AutoField(primary_key=True)
	job_no = models.IntegerField(unique = True)

class Lab(models.Model):
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	#tags = TagField()

	def __unicode__(self):
        	return self.name

class DynamicChoiceField(forms.ChoiceField): 
    def clean(self, value): 
        return value

class Field(models.Model):
	lab = models.ForeignKey(Lab)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	#tags = TagField()

	def __unicode__(self):
        	return self.name

class MyForm(forms.Form): 
	field = forms.ModelChoiceField(Field.objects, widget=forms.Select(attrs={'onchange':'FilterTests();'})) 
	test = DynamicChoiceField(widget=forms.Select(attrs={'disabled':'true'}), choices=(('-1','Select Field'),))

class Test(models.Model):
	#lab = models.ForeignKey(Lab)
	field = models.ForeignKey(Field)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=300)
	quantity = models.IntegerField(blank=True, null=True)
	unit = models.CharField(max_length=15)
	cost = models.IntegerField(blank=True, null=True)
	#tags = TagField()

	def __unicode__(self):
        	return self.name
	
class ClientJob(models.Model):
	"""
	:ClientJob:
	
	ClientJob Class is define all field reqiued to submit detail about new Job.
	
	""" 
        client = models.ForeignKey(UserProfile)
	job_no = models.AutoField(primary_key=True)
	type_of_consultancy = models.CharField(max_length=15,choices=CONSULTANCY_CHOICES)
	date = models.DateField(default=datetime.date.today())
	site = models.CharField(max_length=600, blank=True )
	field = models.ForeignKey(Field)
	material = models.ManyToManyField(Test, related_name="test")
	#type_of_organisation = models.CharField(max_length=20,choices=ORGANISATION_CHOICES)
	type_of_work = models.CharField(max_length=20,choices=ORGANISATION_CHOICES)
	report_type = models.CharField(max_length=20,choices=REPORT_TYPE)


class ClientJobForm(forms.Form):
	fields = forms.ModelChoiceField(queryset = Field.objects.order_by('name'))
#	material = DynamicMultipleChoiceField(widget = forms.CheckboxSelectMultiple(), choices = [])

	def filter_features(self, data):
		tests = Test.objects.order_by('name')
		query = data.get('filter_field_id', 0)

		if query:
			field = Field.objects.get(pk = query)
			tests = tests.filter(field_id = field)

		self.fields['material'].choices = [ (test.pk, test.name) for test in tests ] 

class TestsForm(ModelForm):

    tests = forms.ModelMultipleChoiceField(queryset=Test.objects.all(), required=False,widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ClientJob
	exclude = ('report_type','type_of_consultancy','field','client','date','site','type_of_work','letter_no','letter_date',)

    def __init__(self):
        super(TestsForm, self).__init__()
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	field = Field.objects.all()
	client = ClientJob.objects.values_list('field_id',flat=True).filter(job_no = maxid)
        self.fields['tests'].queryset = Test.objects.filter(field_id = client)

class Amount(models.Model):
	job_no = models.ForeignKey(ClientJob)
	#date = models.DateField(default=datetime.date.today(), editable=False)
	lab = models.ForeignKey(Lab)
	college_income = models.IntegerField(blank=True, null=True)
	admin_charge = models.IntegerField(blank=True,null=True)
	consultancy_asst = models.IntegerField(blank=True,null=True)
	development_fund = models.IntegerField(blank=True,null=True)
	total = models.IntegerField(blank=True,null=True)
	education_tax = models.IntegerField(blank=True,null=True)
	higher_education_tax = models.IntegerField(blank=True,null=True)
	service_tax = models.IntegerField(blank=True,null=True)
	net_total = models.IntegerField(blank=True,null=True)
	tds = models.IntegerField(blank=True,null=True)
	balance = models.IntegerField(blank=True,null=True)
	field = models.ForeignKey(Field)
	#field = models.CharField(max_length=100,choices=FIELD_CHOICES)
	other_field = models.CharField(max_length=100,blank=True,null=True)
	report_type = models.CharField(max_length=20,editable=False)
        type = models.CharField(max_length=10, choices=PAYMENT_CHOICES) 
   
        def __unicode__(self):
          return self.id()



class AmountForm(ModelForm):
	class Meta :
		model = Amount

class CdfAmount(models.Model):
	job_no = models.IntegerField(primary_key=True, editable =False)
	date = models.DateField(default=datetime.date.today(), editable=False)
	lab = models.CharField(max_length=100)
	total = models.IntegerField()
	field = models.CharField(max_length=10)
	other_field = models.CharField(max_length=100,blank=True,null=True)
	report_type = models.CharField(max_length=20,editable=False)

class CdfAmountForm(ModelForm):
	class Meta :
		model = CdfAmount	
	
class Suspence(models.Model):
	job_no = models.ForeignKey(ClientJob)
	type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
	check_number = models.CharField(max_length=15,blank=True)
	check_dd_date = models.CharField(blank=True, max_length=15)
	work_charge = models.IntegerField(null=True, blank=True)
	labour_charge = models.IntegerField( blank=True, null=True)
	boring_charge_external = models.IntegerField( blank=True, null=True)
	boring_charge_internal = models.IntegerField( blank=True, null=True)
	car_taxi_charge = models.IntegerField( blank=True, null=True)
	lab_testing_staff = models.CharField( max_length=90,blank=True)
	field_testing_staff =models.CharField( max_length=90,blank=True)
	test_date = models.DateField( blank=True, null=True)
	suspence_bill_no = models.IntegerField( blank=True, null=True)

class SuspenceForm(ModelForm):
	class Meta :
		model = Suspence


class Organisation(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	accrediatoin = models.CharField(max_length=200)
	fax = models.CharField(max_length=20)
	e_mail = models.CharField(max_length=80)
	director = models.CharField(max_length=50) 
	logo_upload = models.ImageField(upload_to='logo')

	def __unicode__(self):
        	return self.name

class Department(models.Model):
	organisation = models.ForeignKey(Organisation)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=150)
	phone = models.CharField(max_length=20)
	dean = models.CharField(max_length=50)
	faxno = models.IntegerField( blank=True, null=True)

	def __unicode__(self):
        	return self.name

class Staff(models.Model):
	department = models.ForeignKey(Department)
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=50)
	daily_income = models.IntegerField(blank=True)
	position = models.CharField(max_length=15)
	lab = models.ForeignKey(Lab)
	email =models.EmailField(blank=True)
	

class Proformabill(models.Model):
	pro_no = models.AutoField(primary_key=True)
	name = models.CharField(max_length=210)
	address = models.CharField(max_length=750)
	charges_for = models.CharField(max_length=450)
	site = models.CharField(max_length=750)
	sample = models.CharField(max_length=270)
	ref_no = models.CharField(max_length=300)
	rate = models.IntegerField()
	amount = models.IntegerField()
	date = models.DateField(default=datetime.date.today())
	transpotation = models.IntegerField()
	labour = models.CharField(max_length=300)


class ProformabillForm(ModelForm):
	class Meta :
		model = Proformabill
                widgets = {
             'name' : TextInput(attrs={'size':60}),
             'address' : TextInput(attrs={'size':60}),
             'charges_for' : TextInput(attrs={'size':60}),
             'site' : TextInput(attrs={'size':60}),
             'sample' : TextInput(attrs={'size':60}),
             'ref_no' : TextInput(attrs={'size':60}),
             'rate' : TextInput(attrs={'size':60}),
             'amount' : TextInput(attrs={'size':60}),
             'date' : TextInput(attrs={'size':60}),
             'transpotation' : TextInput(attrs={'size':60}),
             'labour' : TextInput(attrs={'size':60}),
         }

class ProfromaTax(models.Model):
    pro_no = models.IntegerField(primary_key=True)
    service_tax = models.IntegerField()
    higher_education_tax = models.IntegerField()
    education_tax = models.IntegerField()
    total = models.IntegerField()

class Ta_Da(models.Model):
	"""
	Model of TA/DA Report
	"""
	id = models.AutoField(primary_key=True)
	job_no = models.IntegerField()
	departure_time_up = models.TimeField(default = "00:00:00") 
	arrival_time_up = models.TimeField(default = "00:00:00") 
	departure_time_down = models.TimeField(default = "00:00:00")
	arrival_time_down = models.TimeField(default = "00:00:00") 
	tada_amount = models.IntegerField(blank=True, null=True, editable=False)
	reach_site = models.CharField(max_length=60, blank=True)
	test_date = models.CharField(default='0000-00-00', max_length=15)
	end_date = models.CharField(max_length=15)
	testing_staff_code_1 = models.CharField(max_length=4)
	testing_staff_code_2 = models.CharField(max_length=4, blank=True)
	testing_staff_code_3 = models.CharField(max_length=4, blank=True)
	testing_staff_code_4 = models.CharField(max_length=4, blank=True)
	testing_staff_code_5 = models.CharField(max_length=4, blank=True)
	testing_staff_code_6 = models.CharField(max_length=4, blank=True)
	testing_staff_code_7 = models.CharField(max_length=4, blank=True)
	testing_staff_code_8 = models.CharField(max_length=4, blank=True)
	testing_staff_code_9 = models.CharField(max_length=4, blank=True)
	testing_staff_code_10 = models.CharField(max_length=4, blank=True)

class Ta_DaForm(ModelForm):
	class Meta :
		model = Ta_Da
		widgets = {
            'testing_staff_code_1': TextInput(attrs={'size': 1}),
            'testing_staff_code_2': TextInput(attrs={'size': 1}),
            'testing_staff_code_3': TextInput(attrs={'size': 1}),
            'testing_staff_code_4': TextInput(attrs={'size': 1}),
            'testing_staff_code_5': TextInput(attrs={'size': 1}),
            'testing_staff_code_6': TextInput(attrs={'size': 1}),
            'testing_staff_code_7': TextInput(attrs={'size': 1}),
            'testing_staff_code_8': TextInput(attrs={'size': 1}),
            'testing_staff_code_9': TextInput(attrs={'size': 1}),
            'testing_staff_code_10': TextInput(attrs={'size': 1}),
        }

class Transportation(models.Model):
	vehicleno = models.CharField(max_length=150)
	rate = models.IntegerField(default='7')

class Transport(models.Model):
	"""
	Model of Transport  Bill record
	"""
	vehicle = models.ForeignKey(Transportation)
	id = models.AutoField(primary_key=True)
	job_no = models.IntegerField()
	bill_no = models.IntegerField(null=True, editable=False)
	kilometer = models.CharField(max_length=150, default="00, 00, 00")
	#rate = models.IntegerField(default='4')
	amounts = models.CharField(max_length=180, blank=True,editable=False)
	total = models.IntegerField(blank=True, null=True , editable=False)
	date = models.DateField(default=datetime.date.today())
	test_date = models.CharField(max_length=300, default="0000-00-00, 0000-00-00")

class TransportForm(ModelForm):
	class Meta :
		model = Transport

class Bankdetails(models.Model):
	accname = models.CharField(max_length=50)
	accountno = models.IntegerField(null=False)
	accountcode = models.CharField(max_length=50)
	address = models.CharField(max_length=150)
'''
################################
#table for testing purpose only#
################################
class test(models.Model):
#	head1 = models.ForeignKey(head)
	test_column1 = models.CharField(max_length=255)
	refrence_table = models.CharField(max_length=255)    

class testForm(ModelForm):
	class Meta :
		model = test
'''
