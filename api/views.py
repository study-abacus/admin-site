from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)

from form import models
from api import serializer

# Create your views here.

class CentreList(ListAPIView):
    queryset = models.Centre.objects.all()
    serializer_class = serializer.CenterSerializer

class CreateContactQuery(CreateAPIView):
    serializer_class = serializer.ContactQuerySerializer

class ExamsList(ListAPIView):
    queryset = models.Exams.objects.all()
    serializer_class = serializers.ExamSerializer
