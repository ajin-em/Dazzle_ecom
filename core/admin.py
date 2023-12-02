from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Django admin class for the CustomUser model.

    This class customizes the Django admin interface for the CustomUser model.
    It includes fields for email, username, is_active, is_staff, and is_blocked in the list view.
    It also includes filters for is_active, is_staff, and is_blocked, and a search box for email and username.
    It provides action methods to ban and unban selected users.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        list_filter (tuple): The fields to filter in the list view.
        search_fields (tuple): The fields to search in the list view.
        actions (list): The action methods to apply to selected users.

    Methods:
        ban_user(self, request, queryset): Ban selected users.
        unban_user(self, request, queryset): Unban selected users.
    """

    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_blocked')
    list_filter = ('is_active', 'is_staff', 'is_blocked')
    search_fields = ('email', 'username')

    def ban_user(self, request, queryset):
        """
        Ban selected users.

        This method sets the is_blocked field of the selected users to True.

        Args:
            request (HttpRequest): The current Django HttpRequest object.
            queryset (QuerySet): The set of selected users.

        Returns:
            None
        """
        queryset.update(is_blocked=True)

    def unban_user(self, request, queryset):
        """
        Unban selected users.

        This method sets the is_blocked field of the selected users to False.

        Args:
            request (HttpRequest): The current Django HttpRequest object.
            queryset (QuerySet): The set of selected users.

        Returns:
            None
        """
        queryset.update(is_blocked=False)

    ban_user.short_description = "Ban selected users"
    unban_user.short_description = "Unban selected users"

    actions = [ban_user, unban_user]
