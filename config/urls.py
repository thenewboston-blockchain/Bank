from django.contrib import admin
from django.urls import include, path

admin.site.index_title = 'Admin'
admin.site.site_header = 'Bank'
admin.site.site_title = 'Bank'

urlpatterns = [

    # Core
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # API (v1)
    path('', include('v1.banks.urls')),
    path('', include('v1.bank_transactions.urls')),
    path('', include('v1.members.urls')),
    path('', include('v1.registrations.urls')),
    path('', include('v1.self_configurations.urls')),
    path('', include('v1.validators.urls')),

]
