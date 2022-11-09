from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED, HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ProfileSignupSerializer, ProfileDetailSerializer


class ProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    permission_classes_by_action = {
        'create': (AllowAny,),
        'retrieve': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'update': (IsAuthenticated,),
        'partial_update': (IsAuthenticated,),
    }
    serializer_class = ProfileSignupSerializer
    serializer_action_classes = {
        'create': ProfileSignupSerializer,
        'list': ProfileDetailSerializer
    }

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_anonymous:
            return self.request.user

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer_class()
            user = serializer(queryset)
            return Response(user.data, status=HTTP_200_OK)
        else:
            return Response({'message': 'Not Authorized'}, HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        # TODO: This method will be used to update validations fields in user
        return Response({'message': 'Method not allowed'}, HTTP_405_METHOD_NOT_ALLOWED)
