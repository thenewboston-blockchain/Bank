from django.urls import path

from .views.confirmation_block import ConfirmationBlockView

urlpatterns = [

    # Confirmation blocks
    path('confirmation_blocks', ConfirmationBlockView.as_view()),

]
