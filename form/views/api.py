from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from form.serializers import StudentSerializer
from form import models

@login_required
@api_view(['POST'])
def get_student_list(request):
	from urllib import parse
	import re
	query = parse.unquote(request.POST['query'].strip())
	if re.match('^[a-zA-Z0-9 ]+ ?$', query):
		students = models.Student.objects.filter(
			(Q(name__istartswith=query) | Q(student_id__startswith=query)) &
			(Q(name__istartswith="") if request.user.is_superuser else Q(ci = request.user.id))
		)[:10]
		serializer = StudentSerializer(students, many = True)
		return Response(serializer.data)
	else:
		return HttpResponse("{}")

@login_required
def isIdAvailable(request):
	import re
	if request.method == "POST":
		id = request.POST['id']
		if (re.match('^[0-9]+$', id)):
			if models.Student.objects.filter(pk=id).count() >= 1 :
				return HttpResponse("False")
			else:
				return HttpResponse("True")
		else:
			return HttpResponse("Error")
	else:
		raise Http404()