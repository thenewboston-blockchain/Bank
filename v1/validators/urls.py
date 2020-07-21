from django.urls import path

from .views.validator import ValidatorDetail, ValidatorView

urlpatterns = [

    # Validators
    path('validators', ValidatorView.as_view()),
    path('validators/<str:node_identifier>', ValidatorDetail.as_view()),

]
