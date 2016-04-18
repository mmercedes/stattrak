from django.shortcuts import render
from rest_framework import permissions, viewsets, status, views
from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.contrib.auth import authenticate, login, logout
from stattrak.models import PlayerData
from django.db.models import Sum

import json

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        
        return (permissions.IsAuthenticated(),)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create an account'
        }, status=status.HTTP_400_BAD_REQUEST)

    @detail_route()
    def stats(self, request):
        user = self.get_object()
        types = PlayerDataType.objects.all()
        stats = {}
        for t in types:
            data = PlayerData.objects.filter(player=user, key=t.key).aggregate(Sum('value'))
            stat[t.key] = list(data)
        return Response(stats)
    
    
class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)
        
        email = data.get('email', None)
        password = data.get('password', None)

        print(email, password)
        account = authenticate(email=email, password=password)
        print(account)
        if account is not None:
            if account.is_active:
                login(request, account)
                
                serialized = AccountSerializer(account)
                
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account is not active.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Invalid login information.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
#    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
