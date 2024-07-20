from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from board.models import Board, Category
from board.serializers import BoardSerializer, CategorySerializer

# Create your views here.
class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Board.objects.filter(members__in=[User.objects.get(id=1)]).order_by('created_at') # Todo: exchange User with logged in user
    serializer_class = BoardSerializer
    permission_classes = [] # kann auch leer sein  für eingeloggten user: permissions.IsAuthenticated
    def create(self, request):
        newBoard = Board.objects.create(
            title = request.data.get('title','newBoard'),
        )
        newBoard.members.add(User.objects.get(id=request.data.get('user_id'))), # Todo: exchange User with logged in user
        self.createDefaultCategories(newBoard)
        serialized_Board = BoardSerializer(newBoard).data
        return Response(serialized_Board, content_type='application/json')
    
    def createDefaultCategories(self,newBoard):
        Category.objects.create(title='Backlog', board=newBoard, position=0)
        Category.objects.create(title='In Progress', board=newBoard, position=1)
        Category.objects.create(title='Done', board=newBoard, position=2)
        
    def destroy(self, pk):
        board = Board.objects.get(id=pk)
        board.delete()
        return HttpResponse(f'Board {pk} deleted')
    
        
    def update(self, request, pk):
        board = Board.objects.get(id=pk)
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
        board.members.remove(user) # ToDo exchange User with logged in user
        print('remove user')

    def addUser(self, user, board):
        board.members.add(user) # ToDo exchange User with logged in user
    
    def deleteMembers(self, newMembers,  board):
        oldMembers = board.members.all()
        for member in oldMembers: 
            if member in newMembers: continue 
            else: self.removeUser(member, board) 


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')
    
    def create(self, request):
        board = Board.objects.get(id=request.data.get('board_id'))
        newCategory = Category.objects.create(
            title = request.data.get('title','newCategory'),
            board = board,
            position = Category.objects.filter(board=board).count(),
        )
        serialized_Category = CategorySerializer(newCategory).data
        return Response(serialized_Category, content_type='application/json')
    
    
    def destroy(self, request, pk):
        board = Board.objects.get(id=request.data.get('board_id'))
        category = Category.objects.get(id=pk)
        resp = f'category {pk} not deleted'
        if category in board.categories.all():
            print(pk)
            category.delete()
            resp = f'category {pk} deleted'
        return HttpResponse(resp) #ToDo: send error if board does nit fit
    
    def update(self, request, pk):
        board = Board.objects.get(id=request.data.get('board_id'))
        category = Category.objects.get(id=pk)
        serialized_Category = f'category {pk}: Title not updated'
        if category in board.categories.all() and request.data.get('title') != None:
            category.title = request.data.get('title')
            category.save()
            serialized_Category = CategorySerializer(category).data
        return Response(serialized_Category, content_type='application/json')