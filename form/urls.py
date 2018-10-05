from django.urls import path
from django.conf.urls import url
from form import views

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('students/', views.StudentList.as_view(), name='students'),
	path('student/<int:pk>', views.StudentDetail.as_view(), name='student'),
	path('add_student/', views.StudentAdd.as_view(), name='add_student'),
	path('edit_student/<int:pk>', views.StudentUpdate.as_view(), name='edit_student'),
	path('add_course/<int:student_id>', views.CourseAdd.as_view(), name='add_course'),
	path('edit_course/<int:pk>', views.CourseUpdate.as_view(), name='edit_course'),
	path('delete_course/<int:pk>', views.CourseDelete.as_view(), name='delete_course'),
	path('add_achievement/<int:student_id>', views.AchievementAdd.as_view(), name='add_achievement'),
	path('edit_achievement/<int:pk>', views.AchievementUpdate.as_view(), name='edit_achievement'),
	path('delete_achievement/<int:pk>', views.AchievementDelete.as_view(), name='delete_achievement'),
	path('add_fee/<int:student_id>', views.FeeAdd.as_view(), name='add_fee'),
	path('edit_fee/<int:pk>', views.FeeUpdate.as_view(), name='edit_fee'),
	path('delete_fee/<int:pk>', views.FeeDelete.as_view(), name='delete_fee'),
	path('success/', views.Success.as_view(), name='success'),

	path('get/', views.get_student_list, name='get_student_list'),
	path('isIdAvailable/', views.isIdAvailable, name='idAvailable'),

	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),


]

# urlpatterns = [
# 	#view
# 	url(r'^$', views.index, name='index'),
# 	url(r'^login/?$', views.login_view, name='login'),
# 	url(r'^logout/?$', views.logout_view, name='logout'),
# 	url(r'^add_student/?$', views.add_student, name='add_student'),
# 	url(r'^edit_student/(?P<student_id>[0-9]+)/?$', views.edit_student, name='edit_student'),
# 	url(r'^student/(?P<student_id>[0-9]+)/?$', views.student, name='student'),
# 	url(r'^edit_course/(?P<course_id>[0-9]+)/?$', views.edit_course, name='edit_course'),
# 	#api
# 	url(r'^changeActive/(?P<student_id>[0-9]+)/?$', views.changeActive, name='changeActive'),
# 	url(r'^isIdAvailable/?$', views.isIdAvailable, name='idAvailable'),
# 	url(r'^get/?$', views.get, name='get'),
# 	url(r'^addCourse/(?P<student_id>[0-9]+)/?$', views.addCourse, name='addCourse'),
# 	url(r'^addAchievement/(?P<student_id>[0-9]+)/?$', views.addAchievement, name='addAchievement'),
# 	url(r'^addFee/?$', views.addFee, name='addFee'),
# 	url(r'^deleteCourse/?$', views.deleteCourse, name='deletCourse'),
# 	url(r'^deleteFee/?$', views.deleteFee, name='deletFee'),
# 	url(r'^deleteAchievement/?$', views.deleteAchievement, name='deleteAchievement'),
# 	#excel_import
# 	url(r'^excelImport/(?P<key>[a-zA-Z0-9]+)/?$', views.excelImport, name='excelImport'),
# 	url(r'^excelImportFee/(?P<key>[a-zA-Z0-9]+)/?$', views.excelImportFee, name='excelImportFee'),
# ]
