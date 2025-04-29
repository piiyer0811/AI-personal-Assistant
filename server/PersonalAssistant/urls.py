from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("two",views.indextwo,name="index2")
]