from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)

from form import models
from api import models as APIModels
from api import serializer

# Create your views here.

class CentreList(ListAPIView):
    queryset = models.Centre.objects.all()
    serializer_class = serializer.CenterSerializer

class CreateContactQuery(CreateAPIView):
    serializer_class = serializer.ContactQuerySerializer

class ExamsList(ListAPIView):
    queryset = APIModels.Exams.objects.all()
    serializer_class = serializer.ExamSerializer

class ExamsDetail(RetrieveAPIView):
    queryset = APIModels.Exams.objects.all()
    serializer_class = serializer.ExamSerializer
    lookup_field = 'slug'
