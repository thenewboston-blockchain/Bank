from django.urls import path

from .views.block import BlockView

urlpatterns = [

    # Blocks
    path('blocks', BlockView.as_view()),

]
