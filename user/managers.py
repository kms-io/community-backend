from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        if not email:
            raise ValueError("Email field must be set")
        if not user_name:
            raise ValueError("Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None):
        user = self.create_user(email, user_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def set_password(self, user, old_password, new_password):
        if not user.check_password(old_password):
            raise ValidationError({"old_password": ["Wrong password."]})
        validate_password(new_password, user=user)
        user.set_password(new_password)
        user.save(using=self._db)
        return user
