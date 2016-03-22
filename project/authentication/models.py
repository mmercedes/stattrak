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
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    bio = models.CharField(max_length=140, blank=True)
    pic = models.CharField(blank=True, max_length=256)
    rating = models.IntegerField()
    sendReport = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AccountManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __unicode__(self):
        return self.username
    
    def getName(self):
        return ' '.join([self.first_name, self.last_name])

