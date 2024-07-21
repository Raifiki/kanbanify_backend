from rest_framework.permissions import BasePermission

from board.models import Board

class isUserMemberOfBoard(BasePermission):
    def has_permission(self, request, view):
        # Check if the user making the request is a member of the board
        if request.query_params.get('board'):
            user = request.user
            board = Board.objects.get(id = request.query_params.get('board'))
            return user in board.members.all()
        else:
            return False