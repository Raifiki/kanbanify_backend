from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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


