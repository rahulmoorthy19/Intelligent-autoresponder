from django.db import models
from django.conf import settings

# Create your models here.

class Username(models.Model):
	name=models.CharField(max_length=10)			##Name of the user                            
	phone_no=models.CharField(max_length=12)		##Phone number of the user				
	email_id=models.EmailField(max_length=75,primary_key=True)		##Email id of the user

class team(models.Model):
	team_id=models.AutoField(primary_key=True)	##id given to the team
	team_name=models.CharField(max_length=10)	##name of the team
	team_type=models.IntegerField(default=1)	##type of queries solved by the team
	team_email_id=models.EmailField(max_length=75)	##emailid given to the team
	workload=models.IntegerField(default=0)		##number of requests given to the team at present

class query(models.Model):
	query_id=models.AutoField(primary_key=True)				##id given to the query
	email_id=models.EmailField(max_length=75)		##email id of the user
	query_ques=models.TextField()						##query of the user
	answer=models.TextField(blank=True)					##Answer to the query of the user(null allowed)
	query_type=models.IntegerField(default=0)	##Type of query of the user(Service or complain)(0 or 1)
	sys_conf=models.IntegerField(default=1)		##Type of query of the user(Software or hardware)(0 or 1)
	team_assigned_id=models.ForeignKey(team,on_delete=models.CASCADE,default=1) ##team id query is assigned(0 for auto)	
	answered_flag=models.IntegerField(default=1)	##Flag for seeing if the query is answered or unaswered(0 or 1)
	language=models.CharField(max_length=2,default="en")
	
	




