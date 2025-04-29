from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("summarisequeryv1", views.summarise_user_prompt, name="summarise_user_prompt")
]