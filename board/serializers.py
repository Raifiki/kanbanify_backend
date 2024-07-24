from django.contrib.auth.models import Group, User
from rest_framework import serializers
from board.models import Board, Category, Task
	
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
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_from = UserSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Task
        fields = ['id','title','description','assigned_to','created_from','created_at','due_date','priority','label','board','category']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = self.getCorrectDate(instance.created_at)
        representation['due_date'] = self.getCorrectDate(instance.due_date)
        return representation
    
    def getCorrectDate(self, date):
        if date == None:
            return None
        else:
            return date.strftime('%Y-%m-%d')
        
