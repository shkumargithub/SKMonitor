from django.db import models

# Create your models here.


class FSList(models.Model):
    sno = models.SmallIntegerField(default=0)
    hostname = models.CharField(max_length=30)
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    filesystem = models.CharField(max_length=200)
    threshold = models.SmallIntegerField(default=5)
    autoaction = models.BooleanField(default=False)


class URLList(models.Model):
    sno = models.SmallIntegerField(default=0)
    url = models.CharField(max_length=300)
    response_code = models.CharField(max_length=10)
    timeout = models.SmallIntegerField(default=60)
    category = models.CharField(max_length=30)
    frequency = models.SmallIntegerField(default=60)
