from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Student, Course, Fee, Achievement
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, StudentAddForm, StudentAddFormByCi, StudentUpdateForm, CourseAddForm, FeeAddForm, AchievementAddForm, StudentUpdateFormByCi
from django.db.models import Q
from django.core import serializers
from datetime import datetime
import json
import re

# APIs are here

@login_required
def changeActive(request, student_id):
	if request.method == "POST":
		if not request.user.is_superuser:
			try:
				student = Student.objects.get(Q(pk = student_id) & Q(ci = request.user))
			except:
				print("jkdashf")
				raise Http404()
		else:
			try:
				student = Student.objects.get(pk = student_id)
			except:
				raise Http404()
		student.active = request.POST['status']
		student.save()
		return HttpResponse("success")
	else:
		raise Http404()

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
		query = request.POST['query'].strip()
		from urllib import parse as urllib
		query = urllib.unquote(query)
		if (re.match('^[a-zA-Z0-9 ]+ ?$', query)):
			students = Student.objects.filter((Q(name__istartswith=query) | Q(student_id__startswith=query)) & (Q(name__istartswith="") if request.user.is_superuser else Q(ci = request.user.id)))[:10]
			print(students)
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
			if request.user.is_superuser:
				student = Student.objects.get(pk=fee_form.cleaned_data['student_id'])
			else:
				try:
					student = Student.objects.get(Q(pk = fee_form.cleaned_data['student_id']) & Q(ci = request.user))
				except:
					raise Http404()
			date = fee_form.cleaned_data['date']
			amount = fee_form.cleaned_data['amount']
			remarks = fee_form.cleaned_data['remarks']
			fee = Fee.objects.create(student=student, date=date, amount=amount, remarks=remarks)
			return HttpResponse(serializers.serialize("json", [fee, ]))
		else:
			return HttpResponse("{'error':'%s'}" % (fee_form.errors))
	else:
		raise Http404()

@login_required
def addCourse(request, student_id):
	if request.method == 'POST':
		course_form = CourseAddForm(request.POST)
		if course_form.is_valid():
			if request.user.is_superuser:
				student = get_object_or_404(Student, student_id=student_id)
			else:
				try:
					student = Student.objects.get(Q(pk = student_id) & Q(ci = request.user))
				except:
					raise Http404()
			course_type = course_form.cleaned_data['course']
			level = course_form.cleaned_data['level']
			course = Course.objects.create(student=student, course=course_type, level=level)
			return HttpResponse(serializers.serialize("json", [course, ]))
		else:
			return HttpResponse("{'error':'Unable to process'}")
	else:
		raise Http404()

@login_required
def addAchievement(request, student_id):
	if request.method == 'POST':
		achievement_form = AchievementAddForm(request.POST)
		if achievement_form.is_valid():
			if request.user.is_superuser:
				student = get_object_or_404(Student, student_id=student_id)
			else:
				try:
					student = Student.objects.get(Q(pk = student_id) & Q(ci = request.user))
				except:
					raise Http404()
			date = achievement_form.cleaned_data['date']
			score = achievement_form.cleaned_data['score']
			position = achievement_form.cleaned_data['position']
			remarks = achievement_form.cleaned_data['remarks']
			achievement = Achievement.objects.create(student = student, date = date, score = score, position = position, remarks = remarks)
			return HttpResponse(serializers.serialize("json", [achievement, ]))
		else:
			return HttpResponse("{'error':'Unable to process'}")
	else:
		raise Http404()

# @login_required
# def updateLevel(request):
	
# 	if request.method == 'POST':
# 		to_do = int(request.POST['to_do'])
# 		course_id = request.POST['course_id']

# 		response = {
# 			'error': '',
# 			'course': ''
# 		}
# 		if to_do not in (1, -1):
# 			response['error'] = 'Wrong To_Do'
# 		if not re.match('^[0-9]+$', course_id):
# 			response['error'] = 'Incorrect id format'
# 		try:
# 			course = Course.objects.get(pk=course_id)
# 		except:
# 			response['error'] = 'ID doesnt exists'

# 		if response['error'] == '':
# 			if to_do == 1:
# 				course.levelIncrease()
# 			elif to_do == -1:
# 				course.levelDecrease()
# 			course.save()
# 			response['course'] = str(course)

# 		return HttpResponse(json.dumps(response))

# 	else:
# 		raise Http404()

# Create your views here.
@login_required
def index(request):

	#counting number of students
	stu_cnt = Student.objects.count() if request.user.is_superuser else Student.objects.filter(ci = request.user.id).count()

	#get the user name if its admin the name will be hardcoded as admin
	name = "Admin" if request.user.is_superuser else request.user.first_name

	params = {
		'stu_cnt':stu_cnt,
		'name':name
	}

	return render(request, 'form/index.html', params)

@login_required
def edit_course(request, course_id):
	instance = get_object_or_404(Course, pk=course_id)
	if not request.user.is_superuser:
		students = Student.objects.filter(ci = request.user)
		flag = False
		for student in students:
			try:
				if student.course_set.get(pk = course_id):
					flag = True
					break
			except:
				pass
		if not flag:
			raise Http404()
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

	if not request.user.is_superuser and not Student.objects.filter(Q(ci = request.user.id) & Q(pk=student_id)).count() >= 1:
		raise Http404()
		return

	try:
		student = Student.objects.get(pk=student_id)
		courses = student.course_set.all()
		fees = student.fee_set.all().order_by('-date')
		achievements = student.achievement_set.all().order_by('-pk')
		course_form = CourseAddForm(initial = {'student_id':student.student_id})
		fee_form = FeeAddForm(initial = {'student_id':student.student_id})
		achievement_form = AchievementAddForm(initial = {'student_id':student.student_id})

	except:
		raise Http404()

	return render(request, 'form/student.html', {
		'achievement_form' : achievement_form,
		'course_form':course_form, 
		'fee_form':fee_form, 
		'achievements' : achievements,
		'courses':courses, 
		'fees':fees,
		'student':student
	})

@login_required
def edit_student(request, student_id):

	if not request.user.is_superuser and not Student.objects.filter(Q(ci = request.user.id) & Q(pk=student_id)).count() >= 1:
		raise Http404()
		return
	instance = get_object_or_404(Student, student_id=student_id)

	success = True
	if request.method == 'POST':
		request.POST = request.POST.copy()
		request.POST['student_id'] = student_id
		form = StudentUpdateForm(request.POST, instance=instance) if request.user.is_superuser else StudentUpdateFormByCi(request.POST, instance = instance)
		if not request.user.is_superuser:
			print("asdf")
			request.POST['ci'] = request.user
		if form.is_valid():

			# all_fields = [field for field in form.base_fields]

			# not_to_update_fields = ['student_id', 'course', 'level']

			# for field in not_to_update_fields:
			# 	all_fields.remove(field)
			instance.ci=form.cleaned_data['ci'] if request.user.is_superuser else request.user
			instance.name=form.cleaned_data['name']
			instance.gender=form.cleaned_data['gender']
			instance.doe = form.cleaned_data['doe']
			instance.dob = form.cleaned_data['dob']
			instance.clas = form.cleaned_data['clas']
			instance.school = form.cleaned_data['school']
			instance.adhaar = form.cleaned_data['adhaar']
			instance.mobile_f = form.cleaned_data['mobile_f']
			instance.mobile_m = form.cleaned_data['mobile_m']
			instance.father_name = form.cleaned_data['father_name']
			instance.mother_name = form.cleaned_data['mother_name']
			instance.occupation_mother = form.cleaned_data['occupation_mother']
			instance.occupation_father = form.cleaned_data['occupation_father']
			instance.address = form.cleaned_data['address']
			instance.annual_income = form.cleaned_data['annual_income']
			instance.save()
			# form.save()
			return redirect('student', student_id=student_id)
		else:
			success = False
	else:
		form = StudentUpdateForm(instance=instance)

	if request.user.is_superuser:
		form.fields["ci"].queryset = User.objects.filter(is_staff = 0).order_by("first_name")
		form.fields['ci'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)

	args = {
		'form' : form, 
		'student' : instance, 
		'success' : success,
		'personal_tuple' : ("name", "gender", "ci", "doe", "dob", "clas", "school", "adhaar", "address") if request.user.is_superuser else ("name", "gender", "clas", "doe", "dob", "school", "adhaar", "address"),
		'parent_tuple' : ("father_name", "occupation_father", "mobile_f", "mother_name", "mobile_m", "occupation_mother", "annual_income")
	}

	return render(request, 'form/student_edit.html', args)

@login_required
def add_student(request):

	isAdmin = request.user.is_superuser

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

		if isAdmin:
			form = StudentAddForm(request.POST)
		else:
			form = StudentAddFormByCi(request.POST)
			ci = request.user

		if form.is_valid():
			
			course = form.cleaned_data['course']
			level = form.cleaned_data['level']

			student = Student.objects.create(
				student_id=form.cleaned_data['student_id'], 
				ci=form.cleaned_data['ci'] if isAdmin else ci,
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
				address = form.cleaned_data['address'],
				annual_income = form.cleaned_data['annual_income']
			)
			course = Course.objects.create(student=student, course=course, level=level)
			success = True
			form = StudentAddForm() if isAdmin else StudentAddFormByCi()

	else:
		form = StudentAddForm() if isAdmin else StudentAddFormByCi()

	if isAdmin:
		form.fields["ci"].queryset = User.objects.filter(is_staff = 0).order_by("first_name")
		form.fields['ci'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)

	args = {
		'form':form, 
		'success':success,
		'personal_tuple' : ("student_id", "name", "gender", "ci", "doe", "dob", "clas", "school", "adhaar", "address"),
		'parent_tuple' : ("father_name", "occupation_father", "mobile_f", "mother_name", "mobile_m", "occupation_mother", "annual_income"),
		'course_tuple' : ("course", "level")
	}

	return render(request, 'form/student_add_form.html', args)

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
		itr = Student._meta.get_fields()[3:]
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


def excelImportFee(request, key):
	if key == "Ns3qgbIpBBmaoyTNvnOU81ZlQCto7815":
		
		students = Student.objects.all()
		
		return render(request, 'form/excel_import_fee.html', {'students' : students})
	else:
		raise Http404()
