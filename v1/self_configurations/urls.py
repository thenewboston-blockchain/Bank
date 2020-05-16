from django.urls import path

from .views.self_configuration import SelfConfigurationDetail
from .views.self_transaction_fee_tier import SelfTransactionFeeTierView

urlpatterns = [

    # Self configuration
    path('self_configuration', SelfConfigurationDetail.as_view()),

    # Self transaction fee tiers
    path('self_transaction_fee_tiers', SelfTransactionFeeTierView.as_view()),

]
