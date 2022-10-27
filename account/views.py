from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from account.serializers import *


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
        user = request.user
        serializer = UpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAuthView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = ChangeAuthSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Success"})
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAPIView(GenericAPIView):
    
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        user = request.user
        serializer = DeleteSerializer(user)

        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Success"}, status=status.HTTP_204_NO_CONTENT)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
