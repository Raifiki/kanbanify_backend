from django.contrib.auth.models import Group, User
from rest_framework import serializers
from board.models import Board, Category
	
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    board = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = ['id','title','position','board']
        
        
class BoardSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ['id','title','members','categories']
        
