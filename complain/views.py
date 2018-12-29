from django.shortcuts import render
from .models import Username,query,team
import import_ipynb
from .predict import predict3
from .spam_filterer import spam_predict
import mtranslate
from langdetect import detect
from django.conf import settings
from .similarityfortokenassigning import predict
from .querysimilarity import predict1
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
import operator
from django.http import HttpResponse,HttpResponseRedirect
complain=Username()
question=query()
complain_path="/home/sirzechlucifer/machine learning/tcs inframind/IntelligentAutoresponder/autoresponder/complain/complainreq.txt"
service_path="/home/sirzechlucifer/machine learning/tcs inframind/IntelligentAutoresponder/autoresponder/complain/servicereq.txt"


def complain_page(request):					##This View is used to take the Query From the User
	if request.method == 'POST':
		complain.name= request.POST.get('name')
		complain.phone_no= request.POST.get('mobilenumber')
		complain.email_id=request.POST.get('emailid')
		complain.save()
		question.email_id=complain.email_id
		question.query_ques=mtranslate.translate(request.POST.get('query_que'))
		if request.POST.get('query_type')=="Hardware":
			question.sys_conf=1
		else:
			question.sys_conf=0
		question.language=detect(request.POST.get('query_que'))
		question.query_type=predict(request.POST.get('query_que'),complain_path,service_path) #detecting complain or service
		spam_check=spam_predict(question.query_ques)	##This function is used to detect is the query is spam or not
		if spam_check==0:
			question.save()
			subject=request.POST.get('query_type')+" Problem"
			query_question=request.POST.get('query_que')
			email(request,subject,query_question)
			return HttpResponseRedirect('thankyou_page/')
		else:
			return render(request, 'complainportal/complain_page.html') 
	else:
		return render(request, 'complainportal/complain_page.html')


def thankyou_page(request):#This view is used for sending the reply in desired language depending upon question present in KB
	similarity={}
	queries=query.objects.filter(answered_flag=0,sys_conf=question.sys_conf,query_type=question.query_type)
	for x in queries:
		similarity[x.query_id]=predict1(question.query_ques,x.query_ques)
	if bool(similarity):
		id_of_answer=max(similarity.items(), key=operator.itemgetter(1))[0]
		similarity_of_answer=similarity[id_of_answer]
	else:
		similarity_of_answer=0
	if similarity_of_answer>80:
		similarity_present(id_of_answer,request)
	else:
		similarity_notpresent(request)
	return render(request, 'complainportal/thankyou_page.html')

						
def email(request,subject,query_question): #Used for sending email from Customer to Service Desk

	email_from = settings.EMAIL_HOST_USER
	recipient_list = ['rahulmoorthy9.6@gmail.com']
	send_mail( subject, query_question, email_from, recipient_list )
	return render(request,'complainportal/complain_page.html')


def revert(request,subject,reply): #Used for Replying back from Service desk to Customer 
	
	email_host = 'smtp.gmail.com'
	host_port = 587
	email_username = 'jaysid91@gmail.com'
	email_password = 'jaysid12'
	email_use_tls = True
	connection = get_connection(host=email_host, 
                            port=host_port, 
                            username=email_username, 
                            password=email_password, 
                            use_tls=email_use_tls)
	send_mail(subject, reply, 'jaysid91@gmail.com', ['rahulmoorthy9.6@gmail.com'], connection=connection)
	connection.close()
	return render(request,'complainportal/complain_page.html')


def similarity_present(id_of_answer,request):# Used when question present in KB
	answer_queries=query.objects.filter(answered_flag=1,sys_conf=question.sys_conf,query_type=question.query_type)
	ref_query=query.objects.get(query_id=id_of_answer)
	for y in answer_queries:
		if y.query_ques==question.query_ques:
			lang=y.language
			y.answer=ref_query.answer
			y.answered_flag=0
			reply="The answer to your query id "+str(y.query_id)+" is "+ref_query.answer
			subject="Solution of query id "+str(y.query_id)
			revert(request,mtranslate.translate(subject,lang,"auto"),mtranslate.translate(reply,lang,"auto"))
			y.save()


def similarity_notpresent(request): #Used when question not present in KB
	team_name={}
	team_list={}
	answer_queries=query.objects.filter(answered_flag=1,sys_conf=question.sys_conf,query_type=question.query_type)
	for z in answer_queries:
		if z.query_ques==question.query_ques:
			lang=z.language
			team_assign=team.objects.filter(team_type=question.query_type)
			for w in team_assign:
				team_name[w.team_id]=w.workload	
				team_list[w.team_id]=w.team_name
			z.team_assigned_id_id=min(team_name.items(), key=operator.itemgetter(1))[0]
			id_of_ques=z.query_id
			z.save()
			team_assign=team.objects.filter(team_id=z.team_assigned_id_id)
			for m in team_assign:
				no_days=predict3(list([str(question.query_ques),int(m.team_type),int(m.workload)]))#no of days
				reply="Your query id "+str(id_of_ques)+" has been assigned to team "+m.team_name+" and will be solved in "+str(no_days)+" days"
				subject="Query Solving process undergoing for query id "+str(id_of_ques)
				revert(request,mtranslate.translate(subject,lang,"auto"),mtranslate.translate(reply,lang,"auto"))
				m.workload=m.workload+1
				m.save()
	
	
