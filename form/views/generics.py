from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import (
	View,
	DetailView,
	ListView,
	CreateView,
	UpdateView,
	DeleteView,
    TemplateView,
)
from django.contrib.auth.views import PasswordChangeView

from form.mixins import (
    LoginRequiredMixin,
    IsAdminMixin,
)
from form import (
    models, 
    forms,
)

from collections import defaultdict

import re

class Index(LoginRequiredMixin, View):
	def get(self, request):
		students_count = models.Student.objects.count() if request.user.is_superuser else models.Student.objects.filter(ci = request.user.id).count()

		context = {
			"student_count": students_count
		}

		return render(request, 'form/index.html', context)

class Success(TemplateView):
    template_name = 'form/success.html'

class StudentList(LoginRequiredMixin, ListView):
    model = models.Student
    template_name = 'form/students.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_context_data(self):
        context = super(StudentList, self).get_context_data()
        context['search_form'] = forms.StudentSearch(self.request.GET)
        return context

    def get_queryset(self):
        students = super(StudentList, self).get_queryset()
        if not self.request.user.is_superuser:
            students = students.filter(ci = self.request.user)

        kwargs = self.request.GET
        name = '' if 'name' not in kwargs else kwargs['name']
        ci = '' if 'ci' not in kwargs else kwargs['ci']
        try:
            student_id = int(kwargs['student_id'])
        except:
            student_id = ''

        if name != '':
            students = students.filter(name__icontains = name)
        if ci != '':
            students = students.filter(ci__user__first_name__icontains = ci)
        if student_id != '':
            students = students.filter(student_id = student_id)

        sort = '' if 'sort' not in kwargs else kwargs['sort']

        if sort == 'name':
            students = students.extra(select={"lower_name": "lower(name)"}).order_by('lower_name')
        elif sort == 'ci':
            students = students.order_by('ci__user__first_name', 'ci__user__last_name')
        elif  sort == 'student_id':
            students = students.order_by('student_id')

        return students

class StudentDetail(LoginRequiredMixin, DetailView):
    model = models.Student
    template_name = 'form/student.html'
    context_object_name = 'student'

class StudentAdd(LoginRequiredMixin, CreateView):
    model = models.Student
    template_name = 'form/student_add_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('add_student')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.StudentAddForm
        else:
            return forms.StudentAddFormByCi

class StudentUpdate(LoginRequiredMixin, UpdateView):
    model = models.Student
    template_name = 'form/student_edit.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('student', kwargs = {"pk" : self.get_object().pk})

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.StudentUpdateForm
        else:
            return forms.StudentUpdateFormByCi

class CourseAdd(LoginRequiredMixin, CreateView):
    model = models.Course
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.CourseAddForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        obj = form.save(commit = False)

        student_id = self.kwargs['student_id']
        student = get_object_or_404(models.Student, pk = student_id) if self.request.user.is_superuser else get_object_or_404(models.Student, pk = student_id, ci = self.request.user)
        obj.student = student

        obj.save()
        return super().form_valid(form)

class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = models.Course
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.CourseAddForm
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        course = super(CourseUpdate, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not course.student.ci == self.request.user:
                raise Http404
        return course

class CourseDelete(LoginRequiredMixin, DeleteView):
    model = models.Course
    template_name = 'form/delete.html'
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        course = super(CourseDelete, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not course.student.ci == self.request.user:
                raise Http404
        return course

class AchievementAdd(LoginRequiredMixin, CreateView):
    model = models.Achievement
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.AchievementAddForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        obj = form.save(commit = False)

        student_id = self.kwargs['student_id']
        student = get_object_or_404(models.Student, pk = student_id) if self.request.user.is_superuser else get_object_or_404(models.Student, pk = student_id, ci = self.request.user)
        obj.student = student

        obj.save()
        return super().form_valid(form)
    
class AchievementUpdate(LoginRequiredMixin, UpdateView):
    model = models.Achievement
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.AchievementAddForm
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        achievement = super(AchievementUpdate, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not achievement.student.ci == self.request.user:
                raise Http404
        return achievement

class AchievementDelete(LoginRequiredMixin, DeleteView):
    model = models.Achievement
    template_name = 'form/delete.html'
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        achievement = super(AchievementDelete, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not achievement.student.ci == self.request.user:
                raise Http404
        return achievement

class FeeAdd(LoginRequiredMixin, CreateView):
    model = models.Fee
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.FeeAddForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        obj = form.save(commit = False)

        student_id = self.kwargs['student_id']
        student = get_object_or_404(models.Student, pk = student_id) if self.request.user.is_superuser else get_object_or_404(models.Student, pk = student_id, ci = self.request.user)
        obj.student = student

        obj.save()
        return super().form_valid(form)
    
class FeeUpdate(LoginRequiredMixin, UpdateView):
    model = models.Fee
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    form_class = forms.FeeAddForm
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        fee = super(FeeUpdate, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not fee.student.ci == self.request.user:
                raise Http404
        return fee

class FeeDelete(LoginRequiredMixin, DeleteView):
    model = models.Fee
    template_name = 'form/delete.html'
    success_url = reverse_lazy('success')

    def get_object(self, *args, **kwargs):
        fee = super(FeeDelete, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser:
            if not fee.student.ci == self.request.user:
                raise Http404
        return fee

class CIDetail(IsAdminMixin, LoginRequiredMixin, DetailView):
    model = models.CI
    template_name = 'form/ci.html'
    context_object_name = 'ci'

class CIAdd(IsAdminMixin, LoginRequiredMixin, CreateView):
    model = models.CI
    template_name = 'form/ci_add_form.html'
    form_class = forms.CIAddForm
    success_url = reverse_lazy('ci_list')

class CIList(IsAdminMixin, LoginRequiredMixin, ListView):
    model = models.CI
    template_name = 'form/cis.html'
    context_object_name = 'cis'
    paginate_by = 20

class CentreAdd(IsAdminMixin, LoginRequiredMixin, CreateView):
    model = models.Centre
    fields = ('name', 'address')
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        obj = form.save(commit = False)

        ci_id = self.kwargs['ci_id']
        ci = get_object_or_404(models.CI, pk = ci_id)
        obj.ci = ci

        obj.save()
        return super().form_valid(form)

class CentreUpdate(IsAdminMixin, LoginRequiredMixin, UpdateView):
    model = models.Centre
    fields = ('name', 'address')
    template_name = 'form/generic_edit_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('success')

class CentreDelete(IsAdminMixin, LoginRequiredMixin, DeleteView):
    model = models.Centre
    template_name = 'form/delete.html'
    success_url = reverse_lazy('success')

class PasswordChange(PasswordChangeView):
    template_name = 'form/password_change.html'
    success_url = reverse_lazy('index')