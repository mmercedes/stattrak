from rest_framework import serializers
from stattrak.models import League, Team
from authentication.models import Account
from authentication.serializers import AccountSerializer

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('teamSize', 'name', 'logo')

        def create(self, validated_data):
            league = League()
            league.teamSize = validated_data.get('teamSize', league.teamSize)
            league.name = validated_data.get('name', league.name)
            league.logo = validated_data.get('logo', league.logo)
            league.save()
            return league

        def update(self, instance, validated_data):
            instance.teamSize = validated_data.get('teamSize', instance.teamSize)
            instance.name = validated_data.get('name', instance.name)
            instance.logo = validated_data.get('logo', instance.logo)
            instance.save()
            return instance
        
class TeamSerializer(serializers.ModelSerializer):
    players = AccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'players')
        read_only_fields = ('id')

        def create(self, validated_data):
            team = Team()
            team.name = validated_data.get('name', team.name)
            teammates = validated_data.get('players', [])
            for teammate in teammates:
                team.players.add(Accounts.objects.get(username=teammate.username))
            team.save()
            return team

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance
            
