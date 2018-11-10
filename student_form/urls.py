from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('form/', include('form.urls')),

    path('auth/obtain_token', obtain_jwt_token),
    path('auth/refresh_token', refresh_jwt_token),

    path('', RedirectView.as_view(url='/form')),
]
