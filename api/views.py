from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# User registration
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get("last_name")
    if username is None or password is None:
        return Response({'error': 'Username and password required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    
    user = User.objects.create_user(username=username, password=password,email=email,first_name=first_name,last_name=last_name)
    token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=201)

# User login
@api_view(['POST'])
def login(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=400)
    
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

# Profile (protected)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({'username': request.user.username})
