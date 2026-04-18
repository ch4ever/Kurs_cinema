
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('siteuser.urls')),
    path('', include('catalog.urls')),
]
