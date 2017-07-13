from django import forms
from .conf import COURSES, CI
from .models import Student, Course

class LoginForm(forms.Form):
	user = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class StudentUpdateForm(forms.Form):
	student_id = forms.IntegerField(widget=forms.HiddenInput())
	name = forms.CharField(max_length=100, label="Name")
	ci = forms.CharField(max_length=100, label="CI Name", widget=forms.Select(choices=CI))

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
	# student_id = forms.IntegerField(label="Student ID")
	# name = forms.CharField(max_length=100, label="Name")
	# ci = forms.CharField(max_length=100, label="CI Name", widget=forms.Select(choices=CI))
	course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	level = forms.IntegerField(initial=1, label="Level")

	# def __init__(self, *args, **kwargs):
 #        super(StudentAddForm, self).__init__(*args, **kwargs)

 #        # change a widget attribute:
 #        self.fields['dob']

	# def clean(self):
	# 	cleaned_data = super(StudentAddForm, self).clean()
	# 	student_id = cleaned_data.get("student_id")

	# 	try:
	# 		Student.objects.get(pk=student_id)
	# 		self.add_error('student_id', "This ID already exists")
	# 	except:
	# 		pass

class CourseAddForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = '__all__'
		exclude = ('student',)
	# student_id = forms.IntegerField(widget=forms.HiddenInput())
	# course = forms.CharField(max_length=2, widget=forms.Select(choices=COURSES), label="Course")
	# level = forms.IntegerField(initial=1, label="Level")	

class FeeAddForm(forms.Form):
	student_id = forms.IntegerField(widget=forms.HiddenInput())
	date = forms.DateField(widget=forms.SelectDateWidget(years=[y for y in range(2017,2020)]))
	amount = forms.IntegerField(label="Amount")
	remarks = forms.CharField(max_length=50, required=False, label="Remarks")
