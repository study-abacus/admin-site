from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from form import models

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class CISerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.CI
        exclude = ('id',)

class CenterSerializer(ModelSerializer):
    ci = CISerializer()

    class Meta:
        model = models.Centre
        exclude = ('id',)