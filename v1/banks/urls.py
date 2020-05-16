from django.urls import path

from .views.bank import BankView

urlpatterns = [

    # Banks
    path('banks', BankView.as_view()),

]
