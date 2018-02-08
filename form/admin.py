from django.contrib import admin
from .models import Student, Course, Fee, Achievement

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Fee)
admin.site.register(Achievement)