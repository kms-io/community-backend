from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
