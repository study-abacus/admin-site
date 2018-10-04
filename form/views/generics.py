from django.shortcuts import render
from django.views.generic import (
	View,
	DetailView,
	ListView,
	CreateView,
	UpdateView,
	DeleteView,
)

from form.mixins import LoginRequiredMixin
from form import models
from form import forms

class Index(LoginRequiredMixin, View):
	def get(self, request):
		students_count = models.Student.objects.count() if request.user.is_superuser else models.Student.objects.filter(ci = request.user.id).count()

		context = {
			"student_count": students_count
		}

		return render(request, 'form/index.html', context)

class StudentDetail(LoginRequiredMixin, DetailView):
    model = models.Student
    template_name = 'form/student.html'
    context_object_name = 'student'

class StudentAdd(LoginRequiredMixin, CreateView):
    model = models.Student
    template_name = 'form/student_add_form.html'
    context_object_name = 'form'
    success_url = '/'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.StudentAddForm
        else:
            return forms.StudentAddFormByCi

class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Student
    template_name = 'form/student_edit.html'
    context_object_name = 'form'
    success_url = '/'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.StudentUpdateForm
        else:
            return forms.StudentUpdateFormByCi