from django.contrib import admin

# Register your models here.

from paginaInicial.models.login import User
from paginaInicial.models.post import Post


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name')
    fields = (('is_active', 'is_staff'), 'username', ('first_name', 'last_name'),
        'email', 'date_joined')

admin.site.register(User, UserAdmin),


class PostAdmin(admin.ModelAdmin):
    list_display = ('summary','start','end')
    list_filter = ('summary',)
    fields = ['summary','start','end']

admin.site.register(Post,PostAdmin)
admin.site.site_header = 'Calender Admin Panel'
