from django.urls import path

from .views.invalid_block import InvalidBlockView

urlpatterns = [

    # Invalid blocks
    path('invalid_blocks', InvalidBlockView.as_view()),

]
