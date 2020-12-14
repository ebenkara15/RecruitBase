from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

#TODO: Fix relation between models and users

#Base User class of the app
class AppUser(AbstractUser):

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)

    is_profile = models.BooleanField(default=True)
    is_firm = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(verbose_name='date inscription', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='derniere connexion', auto_now_add=True)


    def __str__(self):
        return self.username



class Profile(models.Model):
    user = models.ForeignKey(AppUser, null=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField('date of birth', null=True, blank=True)

    #TODO: Define domain name addresses to be accepted
    email_profile = models.EmailField(unique=True)  

    #TODO: Define job domains list
    profile_domain = models.CharField(max_length=200, null=True, blank=True)

    is_available = models.BooleanField(null=True, blank=True)
    profile_text = models.TextField(max_length=1000, null=True, blank=True)
    cv_file = models.FileField(upload_to='cv_uploads/', null=True, blank=True)

    def __str__(self):
        return self.user.username



class Firm(models.Model):
    user = models.ForeignKey(AppUser, null=True, on_delete=models.CASCADE)
    firm_name = models.CharField(max_length=50, blank=True)
    email_firm = models.EmailField(unique=True)
    firm_domain = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return self.firm_name





