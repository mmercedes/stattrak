from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from rest_framework import permissions, viewsets, status, views
from stattrak.models import *
from stattrak.serializers import LeagueSerializer
from rest_framework.response import Response

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
        serializer = self.serializer_class(self.queryset)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid() && len(queryset) == 0:
            League.objects.create_league(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Unable to create a new league'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )

        if self.request.method = 'GET':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)
