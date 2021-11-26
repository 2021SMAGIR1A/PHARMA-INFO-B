"""PharmacieGarde URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views #new
from Pharmacie import views

from django.contrib import admin
# from Pharmacie.admin import site
# admin.site = site
# admin.autodiscover()


urlpatterns = [
    # path('admin/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), #new
    path('admin/', admin.site.urls),
    # path('pharmacie/', include('Pharmacie.urls')),
    path('', views.home, name="home"),
    path('datasave/', views.saveData, name="data"),
    path('login/', views.login, name="login"),
    path('mapjs/', views.getMapPharma, name="mapjs"),
    path('mePos/', views.mapjs, name="mepos"),
    path('pharmacie/getComPharma/', views.getPharmaCom, name="getPharma"),
]
