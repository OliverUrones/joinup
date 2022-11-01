from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProfileViewSet

router_users = SimpleRouter()

router_users.register(r'signup', ProfileViewSet, basename='signup')
router_users.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path(r'', include(router_users.get_urls())),
]