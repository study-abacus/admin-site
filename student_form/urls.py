from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [

    path('admin/', admin.site.urls),
    path('form/', include('form.urls')),
    path('', RedirectView.as_view(url='/form')),

]
