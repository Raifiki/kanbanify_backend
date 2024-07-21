from django.contrib import admin
from .models import Board, Category, Task

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
        'position',
        ]

admin.site.register(Category, AdminCategory)


class AdminTask(admin.ModelAdmin):
    list_display = [
        'id',
        'created_at',
        'title',
        'assigned_to',
        'created_from',
        'due_date',
        'priority',
        'label',
        'category',
        'board',
        ]

admin.site.register(Task, AdminTask)
