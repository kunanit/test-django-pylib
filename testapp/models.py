from django.db import models

# Create your models here.
class Image(models.Model):
	description = models.CharField(max_length=100,blank=True,default='')