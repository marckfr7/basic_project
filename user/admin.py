from django.contrib import admin
from .models import MyUser

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'username')


admin.site.register(MyUser, UserAdmin)
