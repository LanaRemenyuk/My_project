from django.urls import include, path

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, TagViewSet, MaterialViewSet

app_name = 'api'

router = routers.DefaultRouter()
router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('materials', MaterialViewSet, basename='materials')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]