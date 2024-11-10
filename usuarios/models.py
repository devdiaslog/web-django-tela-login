from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    matricula = models.CharField(max_length=10,blank=True,null=True)
    setor = models.CharField(max_length=100,blank=True,null=True)

    #Modificando campos da AbstractUser
    first_name = models.CharField("Primeiro Nome", max_length=150, blank=True)


    def __str__(self):
      return self.username