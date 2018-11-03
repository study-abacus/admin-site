from rest_framework.generics import (
    ListAPIView
)

from form import models
from api import serializer

# Create your views here.

class CentreList(ListAPIView):
    queryset = models.Centre.objects.all()
    serializer_class = serializer.CenterSerializer