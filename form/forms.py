from django import forms
from .conf import COURSES, CI
from .models import Student, Course, Achievement


class LoginForm(forms.Form):
	user = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class StudentUpdateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
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
class StudentUpdateFormByCi(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ('ci',)
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

class StudentAddForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
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
	course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	level = forms.IntegerField(initial=1, label="Level")

class StudentAddFormByCi(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ('ci',)
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
	course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	level = forms.IntegerField(initial=1, label="Level")

class CourseAddForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'
		exclude = ('student',)
	# student_id = forms.IntegerField(widget=forms.HiddenInput())
	# course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	# level = forms.IntegerField(initial=1, label="Level")	

class AchievementAddForm(forms.ModelForm):
	class Meta:
		model = Achievement
		fields = '__all__'
		exclude = ('student',)

class FeeAddForm(forms.Form):
	student_id = forms.IntegerField(widget=forms.HiddenInput())
	date = forms.DateField(widget=forms.SelectDateWidget(years=[y for y in range(2016,2020)]))
	amount = forms.IntegerField(label="Amount")
	remarks = forms.CharField(max_length=50, required=False, label="Remarks")
