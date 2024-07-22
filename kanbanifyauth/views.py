from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed
from board.serializers import UserSerializer

# Create your views here.

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = self.getAuthCredentials(request)
        serializer = self.serializer_class(data=data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
    def getAuthCredentials(self,request):
        try:
            return {
                'username': User.objects.get(email=request.data.get('email')).username,
                'password': request.data.get('password'),
            }
        except:
            return None
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return [permissions.IsAuthenticated()]
    
    def create(self, request):
        if not self.validateData(request.data): return HttpResponse('Missing data', status=400)
        username, email, password, passwordRepeat, first_name, lastt_name = self.getData(request.data)
        if password != passwordRepeat: return HttpResponse('Passwords do not match', status=400)
        if  User.objects.filter(username=username).exists(): return HttpResponse('Username already exists', status=400)
        if User.objects.filter(email=email).exists(): return HttpResponse('Email already exists', status=400)
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = lastt_name
        user.save()
        return  HttpResponse('User created', content_type='text/plain')
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('Cannot delete users')
    
    def validateData(self, data):
        return data.get('username') and data.get('email') and data.get('password') and data.get('passwordRepeat')
    
    def getData(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        passwordRepeat = data.get('passwordRepeat')
        first_name = data.get('firstname')
        last_name = data.get('surename')
        return username, email, password, passwordRepeat, first_name, last_name

