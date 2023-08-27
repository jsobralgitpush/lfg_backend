from django.db import models

# Create your models here.


class Proposal(models.Model):
    name = models.CharField(max_length=100)
    document = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
