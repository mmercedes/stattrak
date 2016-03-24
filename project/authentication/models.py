from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not password:
            raise ValueError('Users must have a password')
        
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')
        
        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        
        account.set_password(password)
        account.save()
        
        return account
    
    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        
        account.is_admin = True
        account.save()
        
        return account
    

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    bio = models.CharField(max_length=140, blank=True)
    pic = models.CharField(blank=True, max_length=256)
    sendReport = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=0)

    objects = AccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __unicode__(self):
        return self.username
    
    def getName(self):
        return ' '.join([self.first_name, self.last_name])

