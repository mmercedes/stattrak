from django.db import models
from authentication import models as auth_models

class League(models.Model):
    teamSize = models.SmallIntegerField()
    name = models.CharField(max_length=100)
    logo = models.CharField(blank=True, max_length=256)
    
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(auth_models.Account)
    name = models.CharField(max_length=30)   

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
    homeTeam = models.ForeignKey('Team', related_name='homeTeam', on_delete=models.CASCADE)
    awayTeam = models.ForeignKey('Team', related_name='awayTeam', on_delete=models.CASCADE)

# Represents a single statistic tied to a single player from a single match 
class PlayerData(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(auth_models.Account, on_delete=models.CASCADE)
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    value = models.IntegerField()

# Represents a single statistic tied to a single team from a single match
class TeamData(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    result = models.ForeignKey('Result', on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    value = models.IntegerField()        
