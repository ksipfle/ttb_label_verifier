from django.urls import path
from . import views

urlpatterns = [
    path("", views.label_form_view, name="label_form"),
]

