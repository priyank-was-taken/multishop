from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenViewBase

from .serializers import LoginSerializer, SignupSerializer


class LoginApiView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class SignupApiView(generics.CreateAPIView):
    # queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
