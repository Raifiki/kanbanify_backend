from django.contrib.auth.models import Group, User
from rest_framework import serializers
from board.models import Board, Category
	
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ['title','members','id']
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title','board','id']
