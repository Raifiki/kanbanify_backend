from django.contrib import admin
from .models import board

# Register your models here.

class AdminBoard(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'get_members',
        'categorylist',
        ]
        
    def get_members(self,obj):
        return "\n".join([member.username for member in obj.members.all()])

admin.site.register(board, AdminBoard)
