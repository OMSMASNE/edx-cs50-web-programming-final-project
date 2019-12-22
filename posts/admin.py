# Copyright (C) 2019 OM SANTOSHKUMAR MASNE. All Rights Reserved.
# Licensed under the GNU Affero General Public License v3.0 only (AGPL-3.0-only) license.
# See License.txt in the project root for license information.

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Custom_User
from .models import Posts

class CustomUserInline(admin.StackedInline):
    model = Custom_User
    can_delete = False
    verbose_name_plural = 'custom_user'

class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.

admin.site.register(Posts)
admin.site.register(Custom_User)
