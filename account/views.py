from rest_framework import response, status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from account.serializers import RegisterSerializer, DetailSerializer



class RegisterAPIView(CreateAPIView):

    serializer_class = RegisterSerializer


class DetailAPIView(GenericAPIView):

    serializer_class = DetailSerializer

    def get(self, request):
        
        ...
