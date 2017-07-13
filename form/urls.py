from django.conf.urls import url
from . import views

urlpatterns = [
	#view
	url(r'^$', views.index, name='index'),
	url(r'^login/?$', views.login_view, name='login'),
	url(r'^logout/?$', views.logout_view, name='logout'),
	url(r'^add_student/?$', views.add_student, name='add_student'),
	url(r'^edit_student/(?P<student_id>[0-9]+)/?$', views.edit_student, name='edit_student'),
	url(r'^student/(?P<student_id>[0-9]+)/?$', views.student, name='student'),
	url(r'^edit_course/(?P<course_id>[0-9]+)/?$', views.edit_course, name='edit_course'),
	#api
	url(r'^isIdAvailable/?$', views.isIdAvailable, name='idAvailable'),
	url(r'^get/?$', views.get, name='get'),
	url(r'^updateLevel/?$', views.updateLevel, name='updateLevel'),
	url(r'^addCourse/(?P<student_id>[0-9]+)/?$', views.addCourse, name='addCourse'),
	url(r'^addFee/?$', views.addFee, name='addFee'),
	url(r'^deleteCourse/?$', views.deleteCourse, name='deletCourse'),
	url(r'^deleteFee/?$', views.deleteFee, name='deletFee'),
	#excel_import
	url(r'^excelImport/(?P<key>[a-zA-Z0-9]+)/?$', views.excelImport, name='excelImport'),
]