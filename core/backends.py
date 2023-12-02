from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend for the CustomUser model.

    This backend checks both the is_active and is_blocked fields during authentication.

    Attributes:
        None

    Methods:
        user_can_authenticate(self, user): Check if the user is active and not blocked.
    """

    def user_can_authenticate(self, user):
        """
        Check if the user is active and not blocked.

        This method returns False if the user is inactive or blocked, and True otherwise.

        Args:
            user (CustomUser): The user to authenticate.

        Returns:
            bool: True if the user is active and not blocked, False otherwise.
        """
        UserModel = get_user_model()
        is_active = getattr(user, 'is_active', False)
        is_blocked = getattr(user, 'is_blocked', False)
        return is_active and not is_blocked