from django.urls import path

from v1.member_registrations.views.member_registration import MemberRegistrationView

urlpatterns = [

    # Member registrations
    path('member_registrations', MemberRegistrationView.as_view()),

]
