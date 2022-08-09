from django.db import models

# Create your models here.
class allup(models.Model):
    upname = models.CharField(max_length=60)
    upsign = models.CharField(max_length=300)

class allvideo(models.Model):
    vtitle = models.CharField(max_length=150)
    vdesc = models.CharField(max_length=1500)