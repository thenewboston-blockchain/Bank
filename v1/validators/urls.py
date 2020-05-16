from django.urls import path

from .views.validator import ValidatorView
from .views.validator_transaction_fee_tier import ValidatorTransactionFeeTierView

urlpatterns = [

    # Validators
    path('validators', ValidatorView.as_view()),

    # Validator transaction fee tiers
    path('validator_transaction_fee_tiers', ValidatorTransactionFeeTierView.as_view()),

]
