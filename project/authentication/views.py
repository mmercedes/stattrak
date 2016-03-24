from django.shortcuts import render
from rest_framework import permissions, viewsets, status, views
from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


import json

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        
        return (permissions.IsAuthenticated(), IsAccountOwner(),)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'Bad request',
            'message': 'Unable to create an account'
        }, status=status.HTTP_400_BAD_REQUEST)

    
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
