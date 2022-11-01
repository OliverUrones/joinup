from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ProfileSignupSerializer, ProfileDetailSerializer
from apps.users.models import Profile


class ProfileViewSet(ModelViewSet):
    permission_classes_by_action = {
        'create': (AllowAny,),
        'retrieve': (IsAuthenticated,)
    }
    serializer_class = ProfileSignupSerializer
    serializer_action_classes = {
        'retrieve': ProfileDetailSerializer
    }

    def get_queryset(self):
        print("get_queryset method")
        if self.action == 'retrieve' and self.request.user:
            return Profile.objects.get(pk=self.kwargs.get('pk'))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        user = serializer(queryset)
        return Response(user.data, status=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        # TODO: This method will be used to update validations fields in user
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)
