from django.db import models

# Create your models here.
class pointRequest(models.Model):
	name= models.CharField(max_length=23)
	chore= models.CharField(max_length=69)
	date= models.CharField(max_length=9)