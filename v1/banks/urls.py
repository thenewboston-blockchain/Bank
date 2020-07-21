from django.urls import path

from .views.bank import BankDetail, BankView

urlpatterns = [

    # Banks
    path('banks', BankView.as_view()),
    path('banks/<str:node_identifier>', BankDetail.as_view()),

]
