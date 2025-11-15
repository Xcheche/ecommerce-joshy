# core/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import transaction
from accounts.models import UserProfile
#from accounts.emails import send_welcome_emails
from django.contrib import messages

from common.tasks import send_welcome_emails


class EmailOrUsernameBackend(ModelBackend):
    """
    Authenticate with either email (primary, since USERNAME_FIELD='email')
    or username. Case-insensitive match. Respects is_active via user_can_authenticate().
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # If a different kwarg was sent (e.g. 'email'), fall back to it
        ident = (username or kwargs.get(UserModel.USERNAME_FIELD) or "").strip()
        if not ident or not password:
            return None

        try:
            user = UserModel._default_manager.get(
                Q(email__iexact=ident) | Q(username__iexact=ident)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None



def create_profile(_backend, user, *_args, **_kwargs):
    if user:  # Ensure user exists
        try:
            with transaction.atomic():
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                )
                
                # Send welcome email
                # send_welcome_emails(user=user)
                if created:
                    messages.info("Created profile for user %s", user.pk)
        except Exception as e:
            messages.error(f"Error creating profile for social auth user: {e}")