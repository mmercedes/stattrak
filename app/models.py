from __future__ import unicode_literals
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django import forms

def override_name(instance, filename):
    return instance.user.username

# Represents a single player in the league
class Player(models.Model):
    user = models.OneToOneField(User)
    phone = moodels.CharField(max_length=10, min_length=10)
    bio = models.CharField(max_length=430)
    pic = models.CharField(blank=True, max_length=256)
    rating = models.IntegerField()
    sendReport = models.BooleanField(default=True)

# Form used to register a new player
class RegisterForm(forms.Form):
    email = forms.CharField(label='email', min_length=3, max_length=255)
    nickname = forms.CharField(label='nickname', min_length=1,  max_length=32)
    f_name = forms.CharField(label='f_name', min_length=1, max_length=32)
    l_name = forms.CharField(label='l_name', min_length=1, max_length=32)
    password = forms.CharField(label='password', min_length=1, max_length=32, widget=forms.PasswordInput)

# Form used to login
class LoginForm(forms.Form):
    username = forms.CharField(label='username', min_length=1,  max_length=32)
    password = forms.CharField(label='password', min_length=1, max_length=32, widget=forms.PasswordInput)

# Form used to edit a player's profile
class EditForm(forms.Form):
    pic = forms.ImageField()
    f_name = forms.CharField(label='f_name', min_length=1, max_length=32)
    l_name = forms.CharField(label='l_name', min_length=1, max_length=32)
    bio = forms.CharField(label='bio', min_length=0, max_length=430)
    phone = models.CharField(max_length=10, min_length=10)
    sendReport = models.BooleanField()

# Represents a group of players in league, players can be on multiple teams
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField("Player")
    name = forms.CharField(min_length=1, max_length=30)

# Represents the result of single match between two teams in the league
class Result(models.Model):
    LOSS = 'L'
    TIE = 'T'
    WIN = 'W'
    OUTCOMES = (
        (LOSS, 'Loss'),
        (TIE, 'Tie'),
        (WIN, 'Win')
    )
    id = models.AutoField(primary_key=True)
    outcome = models.CharField(max_length=1, choices=OUTCOMES)
    homeTeam = models.ForeignKey('Team', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey('Team', on_delete=models.CASCADE)

# Represents a single statistic tied to a single player from a single match 
class PlayerData(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    key = models.CharField(min_length=1, max_length=30)
    value = models.IntegerField()

# Represents a single statistic tied to a single team from a single match
class TeamData(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    key = models.CharField(min_length=1, max_length=30)
    value = models.IntegerField()    

# Represents the configuration of the league
class League(models.Model):
    teamSize = models.SmallIntegerField()
    name = models.CharField(min_length=1, max_length=100)
    logo = models.CharField(blank=True, max_length=256)
    
