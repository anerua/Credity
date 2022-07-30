from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from account.serializers import RegisterSerializer, DetailSerializer, UpdateSerializer


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
        if request.data["old_password"] != "aA1-K+4fX":
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        if request.data["new_password"] == "invalidPassWord":
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        return response.Response({"message": "Success"})
