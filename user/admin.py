from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from.models import User, Group, Member

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'screenname', 'department')}),
		(_('Personal info'), {'fields': (('first_name', 'last_name'), 'email')}),
		(_('Permissions'), {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
	)
	list_display = ['username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
	list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
	search_fields = ['username', 'first_name', 'last_name']
	ordering = ['created_date']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter = ['name']
	search_fields = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ['group', 'user']
	list_display_links = ['group', 'user']
	search_fields = ['group', 'user']
