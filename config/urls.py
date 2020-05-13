from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    # Core
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))

]
