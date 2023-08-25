from django.db import models

# Create your models here.


class Proposal(models.Model):
    name = models.CharField(max_length=100)
    document = models.CharField(max_length=20)
    status = models.CharField(max_length=20)


class CustomAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomAttributeValue(models.Model):
    attribute = models.ForeignKey(CustomAttribute, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    value = models.TextField()

    class Meta:
        unique_together = (('attribute', 'proposal'),)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
