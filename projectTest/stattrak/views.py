from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from rest_framework import permissions, viewsets, status, views
from stattrak.models import *
from stattrak.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from authentication.models import Account

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
    queryset = Team.objects.all()
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
            print teammates
            print 'here'
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
    def stats(self, request):
        team = self.get_object()
        types = TeamDataType.objects.all()
        stats = {}
        for t in types:
            data = TeamData.objects.filter(team=team, key=t.key).aggregate(Sum('value'))
            stat[t.key] = list(data)
        return Response(stats)
    
class PlayerDataTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = PlayerDataType.objects.all()
    serializer_class = PlayerDataTypeSerializer

    def list(self, request):
        serilizer = self.serializer_class(self.queryset, many=True)
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
        serilizer = self.serializer_class(self.queryset, many=True)
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
        
            
            
