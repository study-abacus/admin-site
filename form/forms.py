from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from form.conf import COURSES, CI
from form.models import Student, Course, Achievement, Fee, CI, Centre


class LoginForm(forms.Form):
	user = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class StudentUpdateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ('student_id',)
		labels = {
			'mobile_f' : 'Mobile Number 1',
			'doe' : 'Date of Enrollment',
			'dob' : 'Date of Birth',
			'clas' : 'Class',
			'mobile_m' : 'Mobile Number 2',
		}
		widgets = {
			'doe' : forms.SelectDateWidget(years=[y for y in range(2016,2026)]),
			'dob' : forms.SelectDateWidget(years=[y for y in range(2000,2020)])
		}

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)
		if "ci" in self.fields:
			users = CI.objects.all().order_by('user__first_name', 'user__last_name').exclude(user__first_name = '')
			self.fields['ci'].choices = [(ci.pk, ci.user.get_full_name()) for ci in users]

	def get_personal_fields(self):
		personal = ("student_id", "name", "gender", "father_name", "occupation_father", "mother_name", "occupation_mother", "address", "mobile_f", "mobile_m", "dob", "clas", "school", "ci", "doe", "active")

		fields = []
		for p in personal:
			for field in self:
				if field.name == p:
					fields.append(field)

		return fields

	def get_course_fields(self):
		course =  ("course", "level")
		return [ field for field in self if field.name in course ]


class StudentUpdateFormByCi(StudentUpdateForm):
	StudentUpdateForm.Meta.exclude = ('ci',)

class StudentAddForm(StudentUpdateForm):
	StudentUpdateForm.Meta.exclude = None
	course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	level = forms.IntegerField(initial=1, label="Level")

	def save(self, commit = True):
		obj = super(StudentUpdateForm, self).save(commit = False)

		print(self.cleaned_data)

		if self.is_valid():
			course = Course(
				student = obj,
				course = self.cleaned_data['course'],
				level = self.cleaned_data['level']
			)

		if commit:
			obj.save()
			course.save()
			return obj
		else:
			return obj, course


class StudentAddFormByCi(StudentAddForm):
	StudentAddForm.Meta.exclude = ('ci',)

class StudentSearch(forms.Form):
	student_id = forms.IntegerField(required = False)
	name = forms.CharField(required = False)
	ci = forms.CharField(label = "CI", required = False)

class CourseAddForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'
		exclude = ('student',)

class AchievementAddForm(forms.ModelForm):
	class Meta:
		model = Achievement
		fields = '__all__'
		exclude = ('student',)
		widgets = {
			'date' : forms.SelectDateWidget(years=[y for y in range(2016,2026)])
		}

class FeeAddForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = '__all__'
		exclude = ('student',)
		widgets = {
			'date' : forms.SelectDateWidget(years=[y for y in range(2016,2026)])
		}

class CIAddForm(forms.ModelForm):
	first_name = forms.CharField(max_length = 100)
	last_name = forms.CharField(max_length = 100)
	username = forms.CharField(max_length = 100)
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput())
	centre_name = forms.CharField(max_length = 100)
	centre_address = forms.CharField(widget = forms.Textarea())

	class Meta:
		model = CI
		fields = '__all__'
		exclude = ('user',)

	def save(self, **kwargs):
		ci = super().save(commit=False)

		for field in self.visible_fields():
			if field.name not in self.cleaned_data:
				raise ValidationError(_('{} is required'.format(field.name)), code='invalid')

		user = User(
			username=self.cleaned_data['username'], 
			first_name=self.cleaned_data['first_name'], 
			last_name=self.cleaned_data['last_name'])
		user.set_password(self.cleaned_data['password'])

		centre = Centre(
			name = self.cleaned_data['centre_name'],
			address = self.cleaned_data['centre_address']
		)

		user.save()
		ci.user = user
		ci.save()
		centre.ci = ci
		centre.save()

		return ci
