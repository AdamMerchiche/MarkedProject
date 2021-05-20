from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Communaute(models.Model):
    name = models.CharField(max_length =30)
    abonnes= models.ManyToManyField(User,related_name = "abonnés", blank = True)
    statut = models.BooleanField(default= False)
    def __str__(self):
        return self.name
