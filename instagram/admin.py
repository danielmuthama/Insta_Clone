from django.contrib import admin
from .models import Comment, Post, Like
from django.contrib.auth.admin import UserAdmin

class StyledComment(UserAdmin):
    list_display = ('post','user','body', 'date_posted')
    filter_horizontal = ()
    fieldsets = ()
    ordering = ('-post',)
    list_filter = ()

class StylePost(UserAdmin):
    list_display = ('image','host', 'description', 'date_posted')
    filter_horizontal = ()
    fieldsets = ()
    ordering = ('-date_posted',)
    list_filter = ()


admin.site.register(Comment, StyledComment)
admin.site.register(Post, StylePost)
admin.site.register(Like)