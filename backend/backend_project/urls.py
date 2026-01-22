from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/students/', include('students.urls')),
    # path('api/v1/curriculum/', include('curriculum.urls')), # Commenting out until verified
    path('api/v1/coaching/', include('coaching.urls')),
]
