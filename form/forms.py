from django import forms
from django.contrib.auth.models import User

from form.conf import COURSES, CI
from form.models import Student, Course, Achievement, Fee


class LoginForm(forms.Form):
	user = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class StudentUpdateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ('student_id',)
		labels = {
			'mobile_f' : 'Father\'s Mobile Number',
			'doe' : 'Date of Enrollment',
			'dob' : 'Date of Birth',
			'clas' : 'Class',
			'mobile_m' : 'Mother\'s Mobile Number',
		}
		widgets = {
			'doe' : forms.SelectDateWidget(years=[y for y in range(2016,2020)]),
			'dob' : forms.SelectDateWidget(years=[y for y in range(1990,2018)])
		}

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)
		if "ci" in self.fields:
			users = User.objects.all().order_by('first_name', 'last_name')
			self.fields['ci'].choices = [(user.pk, user.get_full_name()) for user in users]

	def get_personal_fields(self):
		personal = ("student_id", "name", "gender", "ci", "doe", "dob", "clas", "school", "adhaar", "address")
		return [ field for field in self if field.name in personal ]

	def get_parent_fields(self):
		parent =  ("father_name", "occupation_father", "mobile_f", "mother_name", "mobile_m", "occupation_mother", "annual_income")
		return [ field for field in self if field.name in parent ]

	def get_course_fields(self):
		course =  ("course", "level")
		return [ field for field in self if field.name in course ]


class StudentUpdateFormByCi(StudentUpdateForm):
	StudentUpdateForm.Meta.exclude = ('ci',)


class StudentAddForm(StudentUpdateForm):
	StudentUpdateForm.Meta.exclude = None
	course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	level = forms.IntegerField(initial=1, label="Level")


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
			'date' : forms.SelectDateWidget(years=[y for y in range(2016,2020)])
		}

class FeeAddForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = '__all__'
		exclude = ('student',)
		widgets = {
			'date' : forms.SelectDateWidget(years=[y for y in range(2016,2020)])
		}
