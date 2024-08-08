from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='set-password', url_name='set_password')
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
