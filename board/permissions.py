from rest_framework.permissions import BasePermission

from board.models import Board, Category

class isUserMemberOfBoard(BasePermission):
    def has_permission(self, request, view):
        # Check if the user making the request is a member of the board
        if request.query_params.get('board'):
            user = request.user
            board = Board.objects.get(id = request.query_params.get('board'))
            return user in board.members.all()
        else:
            return False
        
class isCategoryInBoard(BasePermission):
    def has_permission(self, request, view):
        # Check if Category is in Board and if the user making the request is a member of the board
        if request.query_params.get('board') and (view.action == 'retrieve' or view.action == 'update' or view.action == 'destroy'):
            pk = view.kwargs.get('pk')
            board = Board.objects.get(id = request.query_params.get('board'))
            category = Category.objects.get(id=pk)
            return category in board.categories.all()
        else:
            return True