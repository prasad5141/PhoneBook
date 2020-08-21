from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)