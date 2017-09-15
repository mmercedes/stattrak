from django.conf.urls import patterns, url, include
from stattrak.views import IndexView, TeamViewSet, LeagueViewSet, PlayerDataTypeViewSet, TeamDataTypeViewSet, ResultViewSet, PlayerDataViewSet, TeamDataViewSet
from rest_framework_nested import routers
from authentication.views import AccountViewSet, LoginView, LogoutView

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'league', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'playerDataTypes', PlayerDataTypeViewSet)
router.register(r'teamDataTypes', TeamDataTypeViewSet)
router.register(r'results', ResultViewSet)
router.register(r'playerData', PlayerDataViewSet)
router.register(r'teamData', TeamDataViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url('^.*$', IndexView.as_view(), name='index'),
)

