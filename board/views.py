from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from board.models import Board, Category, Task
from board.permissions import isCategoryInBoard, isUserMemberOfBoard
from board.serializers import BoardSerializer, CategorySerializer, TaskSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
        
    def list(self , request, *args, **kwargs):
        queryset = Board.objects.filter(members__in=[request.user]).order_by('created_at')
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        newBoard = Board.objects.create(
            title = request.data.get('title','newBoard'),
        )
        newBoard.members.add(request.user),
        self.createDefaultCategories(newBoard)
        serialized_Board = BoardSerializer(newBoard).data
        return Response(serialized_Board, content_type='application/json')
    
    def createDefaultCategories(self,newBoard):
        Category.objects.create(title='Backlog', board=newBoard, position=0)
        Category.objects.create(title='In Progress', board=newBoard, position=1)
        Category.objects.create(title='Done', board=newBoard, position=2)
        
    def destroy(self,request , pk):
        board = Board.objects.get(id=pk)
        if request.user not in board.members.all(): raise MethodNotAllowed('You are not a member of this board')
        board.delete()
        return HttpResponse(f'Board {pk} deleted')
    
        
    def update(self, request, pk):
        board = Board.objects.get(id=pk)
        if request.user not in board.members.all(): raise MethodNotAllowed('You are not a member of this board')
        if request.data.get('title') != None: 
            board.title = request.data.get('title')
            board.save()
        if request.data.get('members') != None:
            membersIdList = request.data.get('members')
            newMembers = User.objects.filter(id__in=membersIdList)
            self.deleteMembers(newMembers,board)
            for member in newMembers: self.addUser(member, board)
        serialized_Board = BoardSerializer(board).data
        return Response(serialized_Board, content_type='application/json')
    
    def removeUser(self, user, board):
        board.members.remove(user)
        print('remove user')

    def addUser(self, user, board):
        board.members.add(user)
    
    def deleteMembers(self, newMembers,  board):
        oldMembers = board.members.all()
        for member in oldMembers: 
            if member in newMembers: continue 
            else: self.removeUser(member, board) 


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, isUserMemberOfBoard, isCategoryInBoard]
    def list(self, request, *args, **kwargs):
        board = Board.objects.get(id = self.request.query_params.get('board'))
        queryset = Category.objects.filter(board = board).order_by('position')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        board = Board.objects.get(id= self.request.query_params.get('board'))
        newCategory = Category.objects.create(
            title = request.data.get('title','newCategory'),
            board = board,
            position = Category.objects.filter(board=board).count(),
        )
        serialized_Category = CategorySerializer(newCategory).data
        return Response(serialized_Category, content_type='application/json')
    
    
    def destroy(self, request, pk):
        board = Board.objects.get(id = self.request.query_params.get('board')) 
        category = Category.objects.get(id=pk)
        resp = f'category {pk} not deleted'
        if category in board.categories.all():
            print(pk)
            category.delete()
            resp = f'category {pk} deleted'
        return HttpResponse(resp) #ToDo: send error if board does nit fit
    
    def update(self, request, pk):
        board = Board.objects.get(id=self.request.query_params.get('board'))
        category = Category.objects.get(id=pk)
        serialized_Category = f'category {pk}: Title not updated'
        if request.data.get('title') != None:
            category.title = request.data.get('title')
            category.save()
            serialized_Category = CategorySerializer(category).data
        return Response(serialized_Category, content_type='application/json')
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, isUserMemberOfBoard]    

    def get_queryset(self):
        board = Board.objects.get(id = self.request.query_params.get('board')) 
        return self.queryset.filter(board=board)

    def list(self , request, *args, **kwargs):
        queryset = self.get_queryset() 
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        board = Board.objects.get(id = self.request.query_params.get('board'))
        assigned_to = User.objects.get(id=request.data.get('assigned_to_id'))
        due_date = datetime.strptime(request.data.get('due_date'), '%Y-%m-%d') if request.data.get('due_date') != None else None
        category = Category.objects.get(id=request.data.get('category_id'))
        resp = 'Task not created: Category not found in board'
        if category in board.categories.all():
            newTask = Task.objects.create(
                title = request.data.get('title','newCategory'),
                description = request.data.get('description',''),
                assigned_to = assigned_to,
                created_from = request.user,
                created_at = datetime.now(),
                due_date = due_date,
                priority = request.data.get('priority','medium'),
                label = request.data.get('label',''),
                category = category,
                board = board,
            )
            resp = TaskSerializer(newTask).data
        return Response(resp, content_type='application/json')
    
    def destroy(self, request, pk):
        board = Board.objects.get(id = self.request.query_params.get('board')) 
        task = Task.objects.get(id=pk)
        resp = f'task {pk} not deleted: Task not found in board'
        if task in board.tasks.all():
            task.delete()
            resp = f'task {pk} deleted'
        return HttpResponse(resp)
    
    def update(self, request, pk):
        board = Board.objects.get(id = self.request.query_params.get('board'))
        task = Task.objects.get(id=pk)
        resp = f'Task {pk} not updated: task not found in board'
        if task in board.tasks.all():
            if request.data.get('title') != None:
                task.title = request.data.get('title')
            if request.data.get('description') != None:
                task.description = request.data.get('description')
            if request.data.get('assigned_to_id') != None:
                user = User.objects.get(id=request.data.get('assigned_to_id'))
                if user in board.members.all(): 
                    task.assigned_to = User.objects.get(id=request.data.get('assigned_to_id'))
            if request.data.get('due_date') != None:
                task.due_date = datetime.strptime(request.data.get('due_date'), '%Y-%m-%d') if request.data.get('due_date') != None else None
            if request.data.get('priority') != None:
                task.priority = request.data.get('priority')
            if request.data.get('label') != None:
                task.label = request.data.get('label')
            if request.data.get('category_id') != None:
                category = Category.objects.get(id=request.data.get('category_id'))
                if category in board.categories.all():
                    task.category = Category.objects.get(id=request.data.get('category_id'))
            task.save()
            resp = TaskSerializer(task).data
        return Response(resp, content_type='application/json')
    
    
