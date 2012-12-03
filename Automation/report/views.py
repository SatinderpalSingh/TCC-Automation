#########################################
# views of the report are described here#
#########################################
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse,HttpResponseRedirect
#from django.db.models import Q
from django.shortcuts import render_to_response
from Automation.report.models import *
from Automation.tcc.models import * 
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.core.context_processors import csrf
from Automation.report.forms import *
#import pdb; pdb.set_trace()

###################################
# For generatin pdf from remplates#
###################################
import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
#from Automation.report.models import soil_ohsr
#################################################

'''
#################################
#simple pdf generation by django#
#################################
def report_pdf(request):
	#Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=report.pdf'

	#Create a PDF object, using the response object as its "file."
	p = canvas.Canvas(response)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, "Guru Nanak Dev Engg College, Ludhiana")

	# Close the PDF object cleanly, and we're done.
	p.showPage()
    	p.save()
  	return response
'''
###############################
#pdf generation bye io library#
###############################
def report_pdf(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=report.pdf'

	buffer = BytesIO()

	# Create the PDF object, using the BytesIO object as its "file."
	p = canvas.Canvas(buffer)	

	# Draw things on the PDF. Here's where the PDF generation happens.
	p.drawString(100, 100, "Guru Nanak Dev Engineering College, Ludhiana")

	# Close the PDF object cleanly.
	p.showPage()
        p.save()

	# Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

'''def report(request):
	query = request.GET.get('q', '')
	if query:
		qset = (
			Q(date_of_testing__icontains=query) |
			Q(type_of_str__icontains=query) |
			Q(latitude_N__icontains=query) |
			Q(longitude_E__icontains=query) |
			Q(presence_1__icontains=query) |
			Q(presence_2__icontains=query) |
			Q(submitted_1__icontains=query) |
			Q(submitted_2__icontains=query) |
			Q(submitted_3__icontains=query) |
			zQ(site_name__icontains=query) |
			Q(water_table__icontains=query)
		)
		results = soil_oshr.objects.filter(qset).distinct()
		else:
			results = []
		return render_to_response("report.html", {
			"results": results,
			"query": query
		})'''
		
#####################
# pdf from templates#
#####################
def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

#####################
#Report of SOIL OHSR#
#####################
def soil_ohsr(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Soil_OhsrFormSet = formset_factory(Soil_OhsrForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Soil_ohsr_formset = Soil_OhsrFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Soil_ohsr_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Soil_ohsr_formset.forms:
                Soil_ohsr = form.save(commit=False)
                Soil_ohsr.Report_id = report
                Soil_ohsr.save()
	
            #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	return HttpResponseRedirect(reverse('Automation.report.views.result_Soil_ohsr'))
    else:
        report_form = ReportForm()
        Soil_ohsr_formset = Soil_OhsrFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Soil_ohsr_formset': Soil_ohsr_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Soil_ohsr(request):
	Id = Soil_Ohsr.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	ohsr = Soil_Ohsr.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/soil_ohsr.html', {'ohsr':ohsr, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

###########################################################################
#to make html file "report_base.html" for a platforms to different reports# 
###########################################################################
def report(request):
	return render_to_response('report/report_base.html', locals())

##########################
#views for the model head#
##########################
def header(request):
		if request.method=='POST':
                	form = headForm(request.POST)
                	if form.is_valid():
                	        cd = form.cleaned_data  
				form.save()
				return HttpResponseRedirect(reverse('Automation.report.views.result'))
				#return render_to_response('report/header.html', {'Head':Head,},context_instance=RequestContext(request))
			else:
		        	return HttpResponse("There was an error with your submission. Please try again.")			
		else:
			form = headForm()
			return render_to_response('report/report.html', {"form":form}, context_instance=RequestContext(request))

def result(request):
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/report_base.html', {'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

###################################	
#views for the model chem_analysis#
###################################
def chemical_analysis(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Chem_analysisFormSet = formset_factory(Chem_analysisForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        chem_analysis_formset = Chem_analysisFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and chem_analysis_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in chem_analysis_formset.forms:
                chem_analysis = form.save(commit=False)
                chem_analysis.Report_id = report
                chem_analysis.save()
	
            #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	return HttpResponseRedirect(reverse('Automation.report.views.result_chem'))
    else:
        report_form = ReportForm()
        chem_analysis_formset = Chem_analysisFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'chem_analysis_formset': chem_analysis_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_chem(request):
	Id = Chem_analysis.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	chem = Chem_analysis.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/chemical_analysis.html', {'chem': chem, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))


'''
def chemical_analysis(request):
	if request.method=='POST':
                	form = chem_analysisForm(request.POST)
                	if form.is_valid():
                	        cd = form.cleaned_data  
				form.save()
				return HttpResponseRedirect(reverse('Automation.report.views.result_chem'))
			else:
		        	return HttpResponse("There was an error with your submission. Please try again.")	
	else:
		form = chem_analysisForm()
		return render_to_response('report/report1.html', {"form":form}, context_instance=RequestContext(request))
		
def result_chem(request):
	Id = chem_analysis.objects.aggregate(Max('id'))
	ID = Id['id__max']
	chem = chem_analysis.objects.filter(id = ID)
	return render_to_response('report/chemical_analysis.html', {'chem': chem,},context_instance=RequestContext(request))
'''
##########################
#views for the model cube#
##########################
'''
def cube_test(request):
	if request.method=='POST':
		form = cubeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
			return HttpResponseRedirect(reverse('Automation.report.views.result_cube'))
		else:
		       	return HttpResponse("There was an error with your submission. Please try again.")	
	else:
		form = cubeForm()
		return render_to_response('report/report3.html', {"form":form}, context_instance=RequestContext(request))

def result_cube(request):
	Id = cube.objects.aggregate(Max('id'))
	ID = Id['id__max']
	cubee = cube.objects.filter(id = ID)
	return render_to_response('report/cube.html', {'cubee':cubee,},context_instance=RequestContext(request))
'''
def index(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    CubeFormSet = formset_factory(CubeForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        todo_item_formset = CubeFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and todo_item_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in todo_item_formset.forms:
                todo_item = form.save(commit=False)
                todo_item.Report_id = report
                todo_item.save()
	
            #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	return HttpResponseRedirect(reverse('Automation.report.views.result_cube'))
    else:
        report_form = ReportForm()
        todo_item_formset = CubeFormSet()
    
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'report_form': report_form,
         'todo_item_formset': todo_item_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_cube(request):
	Id = Cube.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	cubee = Cube.objects.filter(Report_id = ID)
#	return result(request)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/cube.html', {'cubee':cubee, 'Head':Head, 'organisation':organisation},context_instance=RequestContext(request))

################
#view for water#
################
def water_test(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    WaterFormSet = formset_factory(WaterForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        water_formset = WaterFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and water_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in water_formset.forms:
                water = form.save(commit=False)
                water.Report_id = report
                water.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_water'))
    else:
        report_form = ReportForm()
        water_formset = WaterFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'water_formset': water_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_water(request):
	Id = Water.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	water = Water.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/water.html', {'water':water, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

##################
# View for Brick #
##################
def brick_test(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    BrickFormSet = formset_factory(BrickForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        brick_formset = BrickFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and brick_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in brick_formset.forms:
                brick = form.save(commit=False)
                brick.Report_id = report
                brick.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_brick'))
    else:
        report_form = ReportForm()
        brick_formset = BrickFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'brick_formset': brick_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_brick(request):
	Id = Brick.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	brick = Brick.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/brick.html', {'brick':brick, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

##########################
# view for Soil_Building #
##########################
def soil_building(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Soil_BuildingFormSet = formset_factory(Soil_BuildingForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        soil_building_formset = Soil_BuildingFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and soil_building_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in soil_building_formset.forms:
                soil_building = form.save(commit=False)
                soil_building.Report_id = report
                soil_building.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_soil_building'))
    else:
        report_form = ReportForm()
        soil_building_formset = Soil_BuildingFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'soil_building_formset': soil_building_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_soil_building(request):
	Id = Soil_Building.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	Soil_building = Soil_Building.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/soil_building.html', {'Soil_building':Soil_building, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

######################
# View for ADMIXTURE #
######################
def admixture(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    AdmixtureFormSet = formset_factory(AdmixtureForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Mixture_formset = AdmixtureFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Mixture_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Mixture_formset.forms:
                Mixture = form.save(commit=False)
                Mixture.Report_id = report
                Mixture.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_Admixture'))
    else:
        report_form = ReportForm()
        Mixture_formset = AdmixtureFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Mixture_formset': Mixture_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Admixture(request):
	Id = Admixture.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	mixture = Admixture.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/admixture.html', {'mixture': mixture, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# (PPC) IS 1489-1 & 2 Fly Ash Or Clay #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
def cement_ppc(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Cement_PPCFormSet = formset_factory(Cement_PPCForm, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Cement_ppc_formset = Cement_PPCFormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Cement_ppc_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Cement_ppc_formset.forms:
                Cement_ppc = form.save(commit=False)
                Cement_ppc.Report_id = report
                Cement_ppc.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_Cement_PPC'))
    else:
        report_form = ReportForm()
        Cement_ppc_formset = Cement_PPCFormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Cement_ppc_formset': Cement_ppc_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Cement_PPC(request):
	Id = Cement_PPC.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	ppc = Cement_PPC.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/cement_ppc.html', {'ppc': ppc, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

#***********************#
# (OPC) IS 269 33 GRADE #
#***********************#
def cement_opc_33(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Cement_OPC_33FormSet = formset_factory(Cement_OPC_33Form, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Cement_opc_33_formset = Cement_OPC_33FormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Cement_opc_33_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Cement_opc_33_formset.forms:
                Cement_opc_33 = form.save(commit=False)
                Cement_opc_33.Report_id = report
                Cement_opc_33.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_Cement_OPC_33'))
    else:
        report_form = ReportForm()
        Cement_opc_33_formset = Cement_OPC_33FormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Cement_opc_33_formset': Cement_opc_33_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Cement_OPC_33(request):
	Id = Cement_OPC_33.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	opc33 = Cement_OPC_33.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/cement_opc.html', {'opc33': opc33, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

#************************#
# (OPC) IS 8812 43 GRADE # 
#************************#
def cement_opc_43(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Cement_OPC_43FormSet = formset_factory(Cement_OPC_43Form, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Cement_opc_43_formset = Cement_OPC_43FormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Cement_opc_43_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Cement_opc_43_formset.forms:
                Cement_opc_43 = form.save(commit=False)
                Cement_opc_43.Report_id = report
                Cement_opc_43.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_Cement_OPC_43'))
    else:
        report_form = ReportForm()
        Cement_opc_43_formset = Cement_OPC_43FormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Cement_opc_43_formset': Cement_opc_43_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Cement_OPC_43(request):
	Id = Cement_OPC_43.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	opc43 = Cement_OPC_43.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/cement_opc.html', {'opc43': opc43, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

#*************************#
# (OPC) IS 12269 53 GRADE #
#*************************#
def cement_opc_53(request):
    # This class is used to make empty formset forms required
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    Cement_OPC_53FormSet = formset_factory(Cement_OPC_53Form, max_num=30, formset=RequiredFormSet)
    zee = head.objects.aggregate(Max('id'))
    mee = zee['id__max']
    Head = head.objects.get(id = mee)

    if request.method == 'POST': # If the form has been submitted...
        form1 = ReportForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        Cement_opc_53_formset = Cement_OPC_53FormSet(request.POST, request.FILES)
        
        if form1.is_valid() and Cement_opc_53_formset.is_valid():
	   report = form1.save(commit=False)
	   report.Head_id = Head
	   report.save()
           for form in Cement_opc_53_formset.forms:
                Cement_opc_53 = form.save(commit=False)
                Cement_opc_53.Report_id = report
                Cement_opc_53.save()
	
           #return HttpResponseRedirect('thanks') # Redirect to a 'success' page
	   return HttpResponseRedirect(reverse('Automation.report.views.result_Cement_OPC_53'))
    else:
        report_form = ReportForm()
        Cement_opc_53_formset = Cement_OPC_53FormSet()
    
    # For CSRF protection
    c = {'report_form': report_form,
         'Cement_opc_53_formset': Cement_opc_53_formset,
        }
    c.update(csrf(request))
    
    return render_to_response('report/index.html', c)

def result_Cement_OPC_53(request):
	Id = Cement_OPC_53.objects.aggregate(Max('Report_id'))
	ID = Id['Report_id__max']
	opc53 = Cement_OPC_53.objects.filter(Report_id = ID)
	zee = head.objects.aggregate(Max('id'))
	mee = zee['id__max']
	Head = head.objects.all().filter(id = mee)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_response('report/cement_opc.html', {'opc53': opc53, 'Head':Head, 'organisation':organisation,},context_instance=RequestContext(request))

