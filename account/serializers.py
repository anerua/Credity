from rest_framework import serializers
from account.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)
         
        # get the password from the data
        password = data.get('password')
         
        errors = dict() 
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password)
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(RegisterSerializer, self).validate(data)


class DetailSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
