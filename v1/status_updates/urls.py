from django.urls import path

from .views.upgrade_notice import UpgradeNoticeView

urlpatterns = [

    # Upgrade notice (from validator)
    path('upgrade_notice', UpgradeNoticeView.as_view())

]
