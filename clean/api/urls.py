from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet


router = SimpleRouter()
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', include(router.urls))
]