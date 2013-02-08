import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.http import HttpResponseRedirect
from cgi import escape
from Automation.report.views import *
#*******************************************#
#For reportlab
#*******************************************#
from reportlab.graphics.shapes import Drawing,colors
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot


def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def myview(request):
	#Retrieve data or whatever you need	
	#result = Organisation.objects.all().filter(id = 1)
	organisation = Organisation.objects.all().filter(id = 1)
	return render_to_pdf(
	        'report/pdf.html',
	        {
	        	'pagesize':'A4',
#	        	'mylist': result,
			'organisation': organisation,
	        }
	    )
'''
def html_view(request, as_pdf = False):
    #Get varaibles to populate the template
    data = HttpResponseRedirect(reverse('Automation.report.views.result_chem'))
    payload = {'data':data,}
    if as_pdf:
        return payload
    return render_to_response('report/pdf.html', payload, RequestContext(request))

def pdf_view(request):
    payload = html_view(request, as_pdf = True)
    file_data = render_to_string('report/pdf.html', payload, RequestContext(request))
    myfile = StringIO.StringIO()
    pisa.CreatePDF(file_data, myfile)
    myfile.seek(0)
    response =  HttpResponse(myfile, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=coupon.pdf'
    return response
'''

def graph(request):
	buffer = StringIO()
	p = canvas.Canvas(buffer, pagesize = letter)
	
	##### Beginning of code in question
	
	d = Drawing(200, 100)
	pc = Pie()
	pc.x = 65
	pc.y = 15
	pc.width = 70
	pc.height = 70
	pc.data = [10,20,30,40,50,60]
	pc.labels = ['a','b','c','d','e','f']
	pc.slices.strokeWidth=0.5
	pc.slices[3].popout = 10
	pc.slices[3].strokeWidth = 2
	pc.slices[3].strokeDashArray = [2,2]
	pc.slices[3].labelRadius = 1.75
	pc.slices[3].fontColor = colors.red
	d.add(pc)
	
	p.drawPath(d) ### THIS DOES NOT WORK, but need something similar
	
	#####End of Code in Question
	
	p.showPage() #Page Two
	
	p.save() # Saves the PDF and Returns with Response\
	
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response			
