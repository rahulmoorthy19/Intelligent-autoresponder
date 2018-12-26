from django.shortcuts import render
from .models import Username,query
import mtranslate
from langdetect import detect
from django.core.mail import send_mail
from django.conf import settings
from .similarityfortokenassigning import predict

def complain_page(request):
	if request.method == 'POST':
		complain=Username()
		complain.name= request.POST.get('name')
		complain.phone_no= request.POST.get('mobilenumber')
		complain.email_id=request.POST.get('emailid')
		complain.save()
		question=query()
		question.email_id=complain.email_id
		question.query_ques=mtranslate.translate(request.POST.get('query_que'))
		if request.POST.get('query_type')=="Hardware":
			question.sys_conf=1
		else:
			question.sys_conf=0
		question.language=detect(request.POST.get('query_que'))
		question.query_type=predict(request.POST.get('query_que'),"/home/sirzechlucifer/machine learning/tcs inframind/IntelligentAutoresponder/autoresponder/complain/complainreq.txt","/home/sirzechlucifer/machine learning/tcs inframind/IntelligentAutoresponder/autoresponder/complain/servicereq.txt")
		question.save()
		subject=request.POST.get('query_type')+" Problem"
		query_question=request.POST.get('query_que')
		email(request,subject,query_question)
		return render(request, 'complainportal/complain_page.html')  
	else:
		return render(request, 'complainportal/complain_page.html')

def email(request,subject,query_question):

	email_from = settings.EMAIL_HOST_USER
	recipient_list = ['rahulmoorthy9.6@gmail.com']
	send_mail( subject, query_question, email_from, recipient_list )
	return render(request,'complainportal/complain_page.html')

