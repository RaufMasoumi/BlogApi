from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (('Additional', {'fields': ('phone_number', )}, ), )
    add_fieldsets = UserAdmin.add_fieldsets + (('Additional', {'fields': ('phone_number', )}, ), )
    list_display = ['username', 'email', 'is_superuser', 'is_staff', 'phone_number']


admin.site.register(CustomUser, CustomUserAdmin)
