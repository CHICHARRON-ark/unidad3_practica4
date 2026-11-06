from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from users.models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'telefono')


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'telefono', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'telefono')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'telefono', 'password1', 'password2'),
        }),
    )
