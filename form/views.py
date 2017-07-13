from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Student, Course, Fee
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, StudentAddForm, StudentUpdateForm, CourseAddForm, FeeAddForm
from django.db.models import Q
from django.core import serializers
from datetime import datetime
import json
import re

# APIs are here

@login_required
def isIdAvailable(request):

	if request.method == "POST":
		id = request.POST['id']
		if (re.match('^[0-9]+$', id)):
			if Student.objects.filter(pk=id).count() >= 1 :
				return HttpResponse("False")
			else:
				return HttpResponse("True")
		else:
			return HttpResponse("Error")
	else:
		raise Http404()

@login_required
def get(request):

	if request.method == 'POST':

		query = request.POST['query']
		if (re.match('^[a-zA-Z0-9]+ ?$', query)):
			students = Student.objects.filter(Q(name__istartswith=query) | Q(student_id__startswith=query))[:10]
			return HttpResponse(serializers.serialize("json", students))
		else:
			return HttpResponse("{}")

	else:
		raise Http404()

@login_required
def deleteCourse(request):
	if request.method == 'POST':
		response = {
			'error' : ''
		}
		course_id = request.POST['course_id']
		if not re.match('^[0-9]+$', course_id):
			response['error'] = 'Incorrect id format'
		try:
			course = Course.objects.get(pk=course_id)
		except:
			response['error'] = 'ID doesnt exists'

		if response['error'] == '':
			course.delete()

		return HttpResponse(json.dumps(response))

	else:
		raise Http404()

@login_required
def deleteFee(request):
	if request.method == 'POST':
		response = {
			'error' : ''
		}
		fee_id = request.POST['fee_id']
		if not re.match('^[0-9]+$', fee_id):
			response['error'] = 'Incorrect id format'
		try:
			fee = Fee.objects.get(pk=fee_id)
		except:
			response['error'] = 'ID doesnt exists'

		if response['error'] == '':
			fee.delete()

		return HttpResponse(json.dumps(response))

	else:
		raise Http404()	

@login_required
def addFee(request):
	if request.method == 'POST':
		fee_form = FeeAddForm(request.POST)
		if fee_form.is_valid():
			student = Student.objects.get(pk=fee_form.cleaned_data['student_id'])
			date = fee_form.cleaned_data['date']
			amount = fee_form.cleaned_data['amount']
			remarks = fee_form.cleaned_data['remarks']
			fee = Fee.objects.create(student=student, date=date, amount=amount, remarks=remarks)
			return HttpResponse(serializers.serialize("json", [fee, ]))
		else:
			return HttpResponse("{'error':'Unable to process'}")
	else:
		raise Http404()

@login_required
def addCourse(request, student_id):
	if request.method == 'POST':
		course_form = CourseAddForm(request.POST)
		if course_form.is_valid():
			student = get_object_or_404(Student, student_id=student_id)
			course_type = course_form.cleaned_data['course']
			level = course_form.cleaned_data['level']
			course = Course.objects.create(student=student, course=course_type, level=level)
			return HttpResponse(serializers.serialize("json", [course, ]))
		else:
			return HttpResponse("{'error':'Unable to process'}")
	else:
		raise Http404()

@login_required
def updateLevel(request):
	
	if request.method == 'POST':
		to_do = int(request.POST['to_do'])
		course_id = request.POST['course_id']

		response = {
			'error': '',
			'course': ''
		}
		if to_do not in (1, -1):
			response['error'] = 'Wrong To_Do'
		if not re.match('^[0-9]+$', course_id):
			response['error'] = 'Incorrect id format'
		try:
			course = Course.objects.get(pk=course_id)
		except:
			response['error'] = 'ID doesnt exists'

		if response['error'] == '':
			if to_do == 1:
				course.levelIncrease()
			elif to_do == -1:
				course.levelDecrease()
			course.save()
			response['course'] = str(course)

		return HttpResponse(json.dumps(response))

	else:
		raise Http404()

# Create your views here.
@login_required
def index(request):

	#counting number of students
	stu_cnt = Student.objects.count()
	#search suggestions
	students = Student.objects.all()[:10]

	return render(request, 'form/index.html', {'stu_cnt':stu_cnt, 'students':students})

@login_required
def edit_course(request, course_id):
	instance = get_object_or_404(Course, pk=course_id)

	if request.method == "POST":
		form = CourseAddForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return render(request, 'form/course_edit_popup.html', {'form' : form, 'success' : True})

	else:
		form = CourseAddForm(instance=instance)

	return render(request, 'form/course_edit_popup.html', {'form' : form})

@login_required
def student(request, student_id):

	success = False
	if request.method == 'POST':
		form = StudentUpdateForm(request.POST)
		if form.is_valid():
			student = Student.objects.get(pk=form.cleaned_data['student_id'])
			student.name = form.cleaned_data['name']
			student.ci = form.cleaned_data['ci']
			student.save()
			success = True

	try:
		student = Student.objects.get(pk=student_id)
		form = StudentUpdateForm(initial = {
				'student_id' : student.student_id,
				'name' : student.name.upper(),
				'ci' : student.ci.upper()
			})
		courses = student.course_set.all()
		fees = student.fee_set.all().order_by('-date')[:10]
		course_form = CourseAddForm(initial = {'student_id':student.student_id})
		fee_form = FeeAddForm(initial = {'student_id':student.student_id})
	except:
		raise Http404()

	return render(request, 'form/student.html', {
		'form':form,
		'course_form':course_form, 
		'fee_form':fee_form, 
		'courses':courses, 
		'fees':fees,
		'success':success,
		'student':student
	})

@login_required
def edit_student(request, student_id):

	instance = get_object_or_404(Student, student_id=student_id)

	if request.method == 'POST':
		form = StudentAddForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return redirect('student', student_id=student_id)
		else:
			render(request, 'form/student_edit.html', {'form': form, 'student': instance, 'success' : False})

	else:
		form = StudentAddForm(instance=instance)

	return render(request, 'form/student_edit.html', {'form' : form, 'student' : instance})

@login_required
def add_student(request):

	success = False
	if request.method == 'POST':

		#getting the date
		request.POST = request.POST.copy()

		try:
			doe = datetime.strptime(request.POST['doe'], "%d %B, %Y").date()
			request.POST['doe'] = str(doe.month) + "/" + str(doe.day) + "/" + str(doe.year)
		except:
			pass

		try:
			dob = datetime.strptime(request.POST['dob'], "%d %B, %Y").date()
			request.POST['dob'] = str(dob.month) + "/" + str(dob.day) + "/" + str(dob.year)
		except:
			pass

		form = StudentAddForm(request.POST)

		if form.is_valid():
			
			course = form.cleaned_data['course']
			level = form.cleaned_data['level']

			student = Student.objects.create(
				student_id=form.cleaned_data['student_id'], 
				ci=form.cleaned_data['ci'], 
				name=form.cleaned_data['name'],
				gender=form.cleaned_data['gender'],
				doe = form.cleaned_data['doe'],
				dob = form.cleaned_data['dob'],
				clas = form.cleaned_data['clas'],
				school = form.cleaned_data['school'],
				adhaar = form.cleaned_data['adhaar'],
				mobile_f = form.cleaned_data['mobile_f'],
				mobile_m = form.cleaned_data['mobile_m'],
				father_name = form.cleaned_data['father_name'],
				mother_name = form.cleaned_data['mother_name'],
				occupation_mother = form.cleaned_data['occupation_mother'],
				occupation_father = form.cleaned_data['occupation_father'],
				annual_income = form.cleaned_data['annual_income']
			)
			course = Course.objects.create(student=student, course=course, level=level)
			success = True
			form = StudentAddForm()	

	else:
		form = StudentAddForm()

	return render(request, 'form/student_add_form.html', {'form':form, 'success':success})

def logout_view(request):
	if request.user.is_authenticated():
		logout(request)
		return HttpResponseRedirect('/form/login')
	else:
		raise Http404()

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/form')

	invalid = False
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['user']
			password = form.cleaned_data['password']

			user = authenticate(username = username, password = password)

			if user is not None:
				login(request, user)

				try:
					return HttpResponseRedirect(request.GET['next'])
				except:
					return HttpResponseRedirect('/form/')

			else:
				invalid = True

	else:
		
		form = LoginForm()

	return render(request, 'form/login.html', {'form' : form, 'invalid': invalid})

#excel_import
def excelImport(request, key):
	if key == "Ns3qgbIpBBmaoyTNvnOU81ZlQCto7815":
		from django.forms.models import model_to_dict
		itr = Student._meta.get_fields()[2:]
		# students = Student.objects.all()
		students = list()
		for student in Student.objects.all():
			temp = list()
			for field in itr:
				if field.name == "ci":
					temp.append(student.getCi())
				else:
					temp.append(student.serializable_value(field.name))
			temp.append(", ".join([str(course) for course in student.course_set.all()]))
			students.append(temp)
		# students = [ [student.serializable_value(field.name) for field in itr] for student in Student.objects.all()]
		
		return render(request, 'form/excel_import.html', {'students' : students, 'iterator' : itr})
	else:
		raise Http404()

