from django.contrib import admin
from .models import Board, Category

# Register your models here.

class AdminBoard(admin.ModelAdmin):
    list_display = [
        'id',
        'created_at',
        'title',
        'get_members',
        ] 
    def get_members(self,obj):
        return "\n".join([member.username + ' | ' for member in obj.members.all()])

admin.site.register(Board, AdminBoard)


class AdminCategory(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'board',
        ]

admin.site.register(Category, AdminCategory)
