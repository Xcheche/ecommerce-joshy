from django.contrib.auth.tokens import PasswordResetTokenGenerator


"""Activation token generator for email verification links.

Token becomes invalid automatically after activation because `is_active` changes.
"""


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Create a user-specific hash used in activation URLs."""

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
