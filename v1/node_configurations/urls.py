from django.urls import path

from .views.node_configuration import NodeConfigurationDetail

urlpatterns = [

    # Node configuration
    path('node_configuration', NodeConfigurationDetail.as_view()),

]
