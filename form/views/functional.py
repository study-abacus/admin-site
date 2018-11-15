from django.shortcuts import render

from form.models import Student

from decouple import config

KEY = config('EXCEL_IMPORT_KEY', default = 'some_key')

def excelImport(request, key):
	if key == KEY:
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
	if key == KEY:
		
		students = Student.objects.all()
		
		return render(request, 'form/excel_import_fee.html', {'students' : students})
	else:
		raise Http404()