from django.urls import path

from .views.node_configuration import NodeConfigurationDetail
from .views.transaction_fee_tier import TransactionFeeTierView

urlpatterns = [

    # Node configuration
    path('node_configuration', NodeConfigurationDetail.as_view()),

    # Transaction fee tiers
    path('transaction_fee_tiers', TransactionFeeTierView.as_view()),

]
