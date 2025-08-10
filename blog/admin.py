# blog/admin.py
from django.contrib import admin
from .models import User, Tag, Post, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields': ('role',)}),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'publish_date')
    list_filter = ('status', 'publish_date', 'author')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('content',)
