from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')  # 🔍 Add this

# Unregister the original User admin
admin.site.unregister(User)

# Register the customized User admin
admin.site.register(User, CustomUserAdmin)
