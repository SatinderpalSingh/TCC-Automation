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
#	import pdb; pdb.set_trace()

###################################
# For generatin pdf from remplates#
###################################
import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from Automation.report.models import soil_ohsr
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


def soil_ohsr(request):
	if request.method=='POST':
		form = soil_ohsrForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			Date_of_testing = cd['Date_of_testing']
			Type_of_str = cd['Type_of_str']
			Latitude_N = cd['Latitude_N']
			Longitude_E = cd['Longitude_E']
			Presence_1 = cd['Presence_1']
			Presence_2 = cd['Presence_2']
			Submitted_1 = cd['Submitted_1']
			Submitted_2 = cd['Submitted_2']
			Submitted_3 = cd['Submitted_3']
			Site_name = cd['Site_name']
			Water_table = cd['Water_table']
			Depth_D = cd ['Depth_D']
			Diameter_B = cd['Diameter_B']
			Gama_G = cd['Gama_G']
			C = cd['C']
			Phay = cd['Phay']
			Phay_fe = cd['Phay_fe']
			Nc = cd['Nc']
			Nq = cd['Nq']
			Ny = cd['Ny']
			dc = cd['dc']
			dqdy = cd['dqdy']
			Water = cd['Water']
			Pulse_Pulse = cd['Pulse_Pulse']
			Eq_Total = cd['Eq_Total']
			Total_Dby_2 = cd['Total_Dby_2']
			Dt_1 = cd['Dt_1']
			Dt_2 = cd['Dt_2']
			Dt_3 = cd['Dt_3']
			Dt_4 = cd['Dt_4']
			Dt_5 = cd['Dt_5']
			Dt_6 = cd['Dt_6']
			Dt_7 = cd['Dt_7']
			Dt_8 = cd['Dt_8']
			Ob_Pr_1 = cd['Ob_Pr_1']
			Ob_Pr_2 = cd['Ob_Pr_2']
			Ob_Pr_3 = cd['Ob_Pr_3']
			Ob_Pr_4 = cd['Ob_Pr_4']
			Ob_Pr_5 = cd['Ob_Pr_5']
			Ob_Pr_6 = cd['Ob_Pr_6']
			Ob_Pr_7 = cd['Ob_Pr_7']
			Ob_Pr_8 = cd['Ob_Pr_8']
			Corr_F_1 = cd['Corr_F_1']
			Corr_F_2 = cd['Corr_F_2']
			Corr_F_3 = cd['Corr_F_3']
			Corr_F_4 = cd['Corr_F_4']
			Corr_F_5 = cd['Corr_F_5']
			Corr_F_6 = cd['Corr_F_6']
			Corr_F_7 = cd['Corr_F_7']
			Corr_F_8 = cd['Corr_F_8']
			Ob_N_V1 = cd['Ob_N_V1']
			Ob_N_V2 = cd['Ob_N_V2']
			Ob_N_V3 = cd['Ob_N_V3']
			Ob_N_V4 = cd['Ob_N_V4']
			Ob_N_V5 = cd['Ob_N_V5']
			Ob_N_V6 = cd['Ob_N_V6']
			Ob_N_V7 = cd['Ob_N_V7']
			Ob_N_V8 = cd['Ob_N_V8']
			Corr_N_V1 = cd['Corr_N_V1']
			Corr_N_V2 = cd['Corr_N_V2']
			Corr_N_V3 = cd['Corr_N_V3']
			Corr_N_V4 = cd['Corr_N_V4']
			Corr_N_V5 = cd['Corr_N_V5']
			Corr_N_V6 = cd['Corr_N_V6']
			Corr_N_V7 = cd['Corr_N_V7']
			Corr_N_V8 = cd['Corr_N_V8']
			N_Value = cd['N_Value']
			S = cd['S']
			Value = cd['Value']
			Net_Value = cd['Net_Value']
			form.save()
			return render_to_response('report/soil_ohsr.html', {'form': form,
#			return render_to_pdf(
#				'report/report_pdf.html',
#				{
#				'pagesize':'A4',
#                		'mylist':soil_ohsr,
'Date_of_testing':Date_of_testing,
'Type_of_str':Type_of_str,
'Latitude_N':Latitude_N,
'Longitude_E':Longitude_E,
'Presence_1':Presence_1,
'Presence_2':Presence_2,
'Submitted_1':Submitted_1,
'Submitted_2':Submitted_2,
'Submitted_3':Submitted_3,
'Site_name':Site_name,
'Water_table':Water_table,
'Depth_D':Depth_D,
'Diameter_B':Diameter_B,
'Gama_G':Gama_G,
'C':C,
'Phay':Phay,
'Phay_fe':Phay_fe,
'Nc':Nc,
'Nq':Nq,
'Ny':Ny,
'dc':dc,
'dqdy':dqdy,
'Water':Water,
'Pulse_Pulse':Pulse_Pulse,
'Eq_Total':Eq_Total,
'Total_Dby_2':Total_Dby_2,
'Dt_1':Dt_1,
'Dt_2':Dt_2,
'Dt_3':Dt_3,
'Dt_4':Dt_4,
'Dt_5':Dt_5,
'Dt_6':Dt_6,
'Dt_7':Dt_7,
'Dt_8':Dt_8,
'Ob_Pr_1':Ob_Pr_1,
'Ob_Pr_2':Ob_Pr_2,
'Ob_Pr_3':Ob_Pr_3,
'Ob_Pr_4':Ob_Pr_4,
'Ob_Pr_5':Ob_Pr_5,
'Ob_Pr_6':Ob_Pr_6,
'Ob_Pr_7':Ob_Pr_7,
'Ob_Pr_8':Ob_Pr_8,
'Corr_F_1':Corr_F_1,
'Corr_F_2':Corr_F_2,
'Corr_F_3':Corr_F_3,
'Corr_F_4':Corr_F_4,
'Corr_F_5':Corr_F_5,
'Corr_F_6':Corr_F_6,
'Corr_F_7':Corr_F_7,
'Corr_F_8':Corr_F_8,
'Ob_N_V1':Ob_N_V1,
'Ob_N_V2':Ob_N_V2,
'Ob_N_V3':Ob_N_V3,
'Ob_N_V4':Ob_N_V4,
'Ob_N_V5':Ob_N_V5,
'Ob_N_V6':Ob_N_V6,
'Ob_N_V7':Ob_N_V7,
'Ob_N_V8':Ob_N_V8,
'Corr_N_V1':Corr_N_V1,
'Corr_N_V2':Corr_N_V2,
'Corr_N_V3':Corr_N_V3,
'Corr_N_V4':Corr_N_V4,
'Corr_N_V5':Corr_N_V5,
'Corr_N_V6':Corr_N_V6,
'Corr_N_V7':Corr_N_V7,
'Corr_N_V8':Corr_N_V8,
'N_Value':N_Value,
'S':S,
'Value':Value,
'Net_Value':Net_Value
},
context_instance=RequestContext(request))
	else:
  		form = soil_ohsrForm()
	return render_to_response('report/report.html', {"form": form}, context_instance=RequestContext(request))

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
	return render_to_response('report/header.html', {'Head':Head,},context_instance=RequestContext(request))

###################################	
#views for the model chem_analysis#
###################################
def chemical_analysis(request):
		if request.method=='POST':
                	form = chem_analysisForm(request.POST)
                	if form.is_valid():
				cd = form.cleaned_data  
				form.save()
				chem = chem_analysis.objects.all()
				#return HttpResponseRedirect(chem)
				return render_to_response('report/chemical_analysis.html', {'chem': chem,},context_instance=RequestContext(request))
			else:
		        	return HttpResponse("There was an error with your submission. Please try again.")
						
		else:
			form = chem_analysisForm()
			return render_to_response('report/report.html', {"form":form}, context_instance=RequestContext(request))
			
