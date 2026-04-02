"""Custom authentication backends and auth-related helpers for the accounts app.

Feature map:
- `EmailOrUsernameBackend`: lets users sign in with email or username.
- `create_profile`: utility hook to guarantee a profile exists for a user.
"""

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
    Authenticate with either email or username.

    Why this exists:
    - Your `CustomUser` uses `email` as `USERNAME_FIELD`.
    - Many users still try to sign in with a username.

    Behavior:
    - Case-insensitive lookup on both email and username.
    - Password must match.
    - Inactive users are blocked by `user_can_authenticate`.
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
    """Create a `UserProfile` if missing.

    Intended usage:
    - Safe helper for signal/social-auth style hooks.
    - Ensures dashboard/profile pages always have profile data.
    """
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