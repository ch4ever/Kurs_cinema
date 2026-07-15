from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HallViewSet, SeatStatusUpdateView

router = DefaultRouter()
router.register('admin/halls', HallViewSet, basename='halls')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/admin/seats/', SeatStatusUpdateView.as_view(), name='seats-availability'),
]
