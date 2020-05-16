from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    # Core
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # API (v1)
    path('', include('v1.bank_transactions.urls')),
    path('', include('v1.members.urls')),
    path('', include('v1.registrations.urls')),
    path('', include('v1.self_configurations.urls')),
    path('', include('v1.validators.urls')),

]
