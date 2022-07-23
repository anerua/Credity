from dataclasses import fields
from rest_framework import serializers
from account.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")