import eav
from django.db import models
# Create your models here.


class Proposal(models.Model):
    STATUS_CHOICES = (
        ('denied', 'Denied'),
        ('approved', 'Approved'),
        ('pending_by_system', 'Pending by system'),
        ('pending_by_analyst', 'Pending by analyst'),
    )
    name = models.CharField(max_length=100)
    document = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending_by_system')
    last_updated = models.DateTimeField(auto_now=True)


eav.register(Proposal)
