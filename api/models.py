from django.db import models

class ContactQuery(models.Model):
  name = models.CharField(max_length = 256)
  email = models.EmailField()
  phone_number = models.CharField(max_length = 20)
  message = models.TextField()
  
