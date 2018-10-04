from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate

from form.forms import LoginForm

def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		return HttpResponseRedirect('/form/login')
	else:
		raise Http404()

def login_view(request):
	if request.user.is_authenticated:
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