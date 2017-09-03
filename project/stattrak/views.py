from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from rest_framework import permissions, viewsets, status, views
from stattrak.models import *
from stattrak.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from authentication.models import Account
from trueskill import *
from django.db.models import Sum

class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

class LeagueViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            if(len(self.queryset) > 0):
                league = self.queryset[0]
            else:
                league = League()
            league.teamSize = serializer.validated_data.get('teamSize', league.teamSize)
            league.name = serializer.validated_data.get('name', league.name)
            league.logo = serializer.validated_data.get('logo', league.logo)
            league.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create a new league'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        
        if self.request.method is 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    
class TeamViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Team.objects.order_by('name')
    serializer_class = TeamSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            team = Team()
            team.name = serializer.validated_data.get('name', team.name)
            teammates = request.data.get('players', [])
            team.save()
            for teammate in teammates:
                team.players.add(Account.objects.get(username=teammate['username']))
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create a new team'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    @detail_route()
    def stats(self, request, *args, **kwargs):
        team = self.get_object()
        types = TeamDataType.objects.all()
        stats = {}
        for t in types:
            data = TeamData.objects.filter(team=team, key=t.key).aggregate(Sum('value'))
            stats[t.key] = data['value__sum']
        return Response(stats)
    
class PlayerDataTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = PlayerDataType.objects.all()
    serializer_class = PlayerDataTypeSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            playerDT = PlayerDataType()
            playerDT.key = serializer.validated_data.get('key', None)
            playerDT.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create a new player data type'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )

        if self.request.method is 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)    

class TeamDataTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TeamDataType.objects.all()
    serializer_class = TeamDataTypeSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            teamDT = TeamDataType()
            teamDT.key = serializer.validated_data.get('key', None)
            teamDT.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create a new team data type'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )

        if self.request.method is 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)    
        
            
class ResultViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Result.objects.order_by('-id')[:20]
    serializer_class = ResultSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        result = Result()
        result.outcome = request.data.get('outcome', '')
        homeTeam = request.data.get('homeTeam', {})
        awayTeam = request.data.get('awayTeam', {})
        reporter = Account.objects.get(username=request.data.get('reporter',""))
        
        if result.outcome is not '':
            result.homeTeam = Team.objects.get(name=homeTeam['name'])
            result.awayTeam = Team.objects.get(name=awayTeam['name'])
            result.save()
            self.updateRating(result.homeTeam, result.awayTeam, result.outcome)
            return Response(result.id, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to add new result'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )

        if self.request.method is 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)

    def updateRating(self, homeTeam, awayTeam, outcome):
        env = TrueSkill(backend='mpmath')
        homePlayers = homeTeam.players.all()
        awayPlayers = awayTeam.players.all()

        if outcome == 'W':
            teamRanks = [0, 1]
        elif outcome == 'L':
            teamRanks = [1, 0]
        else:
            teamRanks = [0, 0]

        homeRatings = {}
        awayRatings = {}

        for player in homePlayers:
            homeRatings[player.username] = env.create_rating(player.rating)
        for player in awayPlayers:
            awayRatings[player.username] = env.create_rating(player.rating)

        ranked_groups = env.rate([homeRatings, awayRatings], ranks=teamRanks)

        for player in homePlayers:
            player.rating = env.expose(ranked_groups[0][player.username])
            player.save()
        for player in awayPlayers:
            player.rating = env.expose(ranked_groups[1][player.username])
            player.save()
        
class PlayerDataViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = PlayerData.objects.all()
    serializer_class = PlayerDataSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)    

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = PlayerData()
            user = request.data.get('player', {})
            result = request.data.get('result', {})
            data.player = Account.objects.get(username=user['username'])
            data.result = Result.objects.get(id=result['id'])
            data.key = serialzier.validatd_data.get('key', '')
            data.value = serializer.validated_data.get('value', 0)
            data.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to add new player data'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        
        if self.request.method is 'GET':
            return (permissions.AllowAny(),)
        
        return (permissions.IsAuthenticated(),)
    
class TeamDataViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TeamData.objects.all()
    serializer_class = TeamDataSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)    

    def create(self, request):
        data = TeamData()
        team = request.data.get('team', {})
        result = request.data.get('result', {})
        data.team = Team.objects.get(name=team['name'])
        data.result = Result.objects.get(id=result['id'])
        data.key = request.data.get('key', '')
        data.value = request.data.get('value', 0)

        if data.key == '':
            return Response({
                'status': 'Bad Request',
                'message': 'Unable to add new team data'
            }, status=status.HTTP_400_BAD_REQUEST)    

        data.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        
        if self.request.method is 'GET':
            return (permissions.AllowAny(),)
        
        return (permissions.IsAuthenticated(),)    

    
