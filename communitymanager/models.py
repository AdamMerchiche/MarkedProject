from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length =30 )
    first_name = models.CharField(max_length =30 )
    last_name = models.CharField(max_length =30 )
    email = models.EmailField(max_length =30 )


class Communaute(models.Model):
    name = models.CharField(max_length =30 )
    #abonnes=
