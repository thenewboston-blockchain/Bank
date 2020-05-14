from django.urls import path

from .views.member import MemberView

urlpatterns = [

    # Members
    path('members', MemberView.as_view()),

]
