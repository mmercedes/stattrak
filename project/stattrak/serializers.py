from rest_framework import serializers
from stattrak.models import League, Team, PlayerDataType, TeamDataType, PlayerData, TeamData, Result
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
                team.players.add(Account.objects.get(username=teammate.username))
            team.save()
            return team

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance
            
class PlayerDataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerDataType
        fields = ('id', 'key')
        read_only_fields = ('id')

        def create(self, validated_data):
            playerDT = PlayerDataType()
            playerDT.key = serializer.validated_data.get('key', None)
            playerDT.save()
            return playerDT

        def update(self, instance, validated_data):
            instance.key = validated_data.get('key', instance.key)
            instance.save()
            return instance

class TeamDataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamDataType
        fields = ('id', 'key')
        read_only_fields = ('id')

        def create(self, validated_data):
            teamDT = TeamDataType()
            teamDT.key = serializer.validated_data.get('key', None)
            teamDT.save()
            return teamDT

        def update(self, instance, validated_data):
            instance.key = validated_data.get('key', instance.key)
            instance.save()
            return instance        

class PlayerDataSerializer(serializers.ModelSerializer):
    player = AccountSerializer(read_only=True)
    
    class Meta:
        model = PlayerData
        fields = ('id', 'player', 'result', 'key', 'value')
        read_only_fields = ('id')

        def create(self, validated_data):
            data = PlayerData()
            user = validated_data.get('player', {})
            result = validated_data.get('result', {})
            data.player = Account.objects.get(username=user.username)
            data.result = Result.objects.get(id=result.id)
            data.key = validatd_data.get('key', '')
            data.value = validated_data.get('value', 0)
            data.save()
            return data

class TeamDataSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = TeamData
        fields = ('id', 'team', 'result', 'key', 'value')
        read_only_fields = ('id')

        def create(self, validated_data):
            data = TeamData()
            team = validated_data.get('team', {})
            result = validated_data.get('result', {})
            data.team = Team.objects.get(name=team.name)
            data.result = Result.objects.get(id=result.id)
            data.key = validatd_data.get('key', '')
            data.value = validated_data.get('value', 0)
            data.save()
            return data        

        
class ResultSerializer(serializers.ModelSerializer):
    homeTeam = TeamSerializer(read_only=True)
    awayTeam = TeamSerializer(read_only=True)
    reporter = AccountSerializer(read_only=True)
    
    class Meta:
        model = Result
        fields = ('id', 'outcome', 'homeTeam', 'awayTeam', 'reporter')
        read_only_fields = ('id')

        def create(self, validated_data):
            user = validated_data.get('reporter', {})
            data = validated_data
            data.reporter = Account.objects.get(username=user)
            return data

        def update(self, instance, validated_data):
            return

