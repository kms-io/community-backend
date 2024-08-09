from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.AuthView.as_view(), name='Auth'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/set-password/', views.CustomUserViewSet.as_view({'post': 'set_password'}), name='set_password'),
]
