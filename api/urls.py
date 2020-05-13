from django.urls import path

from api import views

urlpatterns = [
    path('centres/', views.CentreList.as_view()),
    path('contact_query/', views.CreateContactQuery.as_view()),
    path('exams/', views.ExamsList.as_view()),
    path('exams/<slug>', views.ExamsDetail.as_view())
]