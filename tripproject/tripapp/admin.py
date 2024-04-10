from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Picture
from .models import Location
from .models import Item
from .models import Memo
from .models import Trip

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff')
    fieldsets = (
        ('ユーザー情報', {'fields': ('username', 'email', 'password')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        ('ユーザー情報',{
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )

admin.site.register(User, CustomizeUserAdmin)

admin.site.register(Picture)
admin.site.register(Location)
admin.site.register(Item)
admin.site.register(Memo)
admin.site.register(Trip)