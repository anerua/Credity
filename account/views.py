from rest_framework import response, status
from rest_framework.generics import GenericAPIView, CreateAPIView
from account.serializers import RegisterSerializer



class RegisterAPIView(CreateAPIView):

    serializer_class = RegisterSerializer


class DetailAPIView(GenericAPIView):

    ...
