from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User, AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.forms import UserCreationForm


class User(AbstractUser):
    """
    Modele pour representer un utilisateur
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username



class Project(models.Model):
    """
    Modèle pour représenter un projet
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

