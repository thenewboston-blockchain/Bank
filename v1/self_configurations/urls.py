from django.urls import path

from .views.self_configuration import SelfConfigurationDetail
from .views.transaction_fee_tier import TransactionFeeTierView

urlpatterns = [

    # Self configuration
    path('self_configuration', SelfConfigurationDetail.as_view()),

    # Transaction fee tiers
    path('transaction_fee_tiers', TransactionFeeTierView.as_view()),

]
