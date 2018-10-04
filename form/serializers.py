from rest_framework import serializers

from form import models

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ('name', 'pk')