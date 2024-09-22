from django.contrib import admin

from apps.user.models import User


# Register your models here.
class UserAdmin(User):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User)
