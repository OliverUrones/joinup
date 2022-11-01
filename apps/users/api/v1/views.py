from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import ProfileSignupSerializer
from apps.users.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSignupSerializer

