from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug' ,'updated_at', 'published_at')
    ordering = ('-published_at',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)