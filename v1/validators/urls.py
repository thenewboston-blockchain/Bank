from django.urls import path

from .views.validator import ValidatorView

urlpatterns = [

    # Validators
    path('validators', ValidatorView.as_view()),

]
