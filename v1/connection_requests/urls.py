from django.urls import path

from .views.connection_request import ConnectionRequestView

urlpatterns = [

    # Connection requests
    path('connection_requests', ConnectionRequestView.as_view()),

]
