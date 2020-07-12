from django.urls import path

from .views.self_configuration import SelfConfigurationDetail

urlpatterns = [

    # Self configuration
    path('config', SelfConfigurationDetail.as_view()),

]
