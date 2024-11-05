from django.urls import path
from . import views

urlpatterns = [path("components", views.components, name="components")]
