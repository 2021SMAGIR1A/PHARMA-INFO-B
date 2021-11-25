from django.urls import path
from . import views
urlpatterns = [
    path('datasave/', views.saveData, name=""),
]