from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "phone_number",
        "role",
    )

    # Fields to filter by in the admin interface
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "role",  # Add role filter if needed
    )

    # Ordering of users in the list view
    ordering = ("role",)

    # Fields to be displayed in the detail view (form)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number", "role")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


# Register the CustomUser model with the CustomUserAdmin class
# admin.site.register(CustomUser, CustomUserAdmin)

