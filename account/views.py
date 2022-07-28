from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from account.serializers import RegisterSerializer, DetailSerializer



class RegisterAPIView(CreateAPIView):

    serializer_class = RegisterSerializer


class DetailAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = DetailSerializer(user)
        return response.Response(serializer.data)
        

class UpdateAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request):
        ...
