from django.urls import path

from .views import user_register, login, CurrentUserView

urlpatterns = [
    path('api/register/', user_register.as_view(), name='register'),
    path('api/login/',login.as_view(), name='login'),
    path('api/getme/',CurrentUserView.as_view(), name='getme'),
]