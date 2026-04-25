from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import User
from .serializers import UserSerializer

class UserAPIView(APIView):
    def get(self, request, pk=None): # Get data or search data
        if pk:
            #Get by pk
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all() # List of object
            serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    
    def post(self, request): 
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthSignUpAPIView(APIView):
    """
    Minimal auth API for the UI:
    - create user with a real password (hashed)
    - return safe user fields (no password)
    """

    def post(self, request):
        username = str(request.data.get("username") or "").strip()
        email = str(request.data.get("email") or "").strip().lower()
        password = str(request.data.get("password") or "")

        if not username or not email or not password:
            return Response(
                {"detail": "username, email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response({"detail": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        serializer = UserSerializer(user)
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthSignInAPIView(APIView):
    def post(self, request):
        username = str(request.data.get("username") or "").strip()
        email = str(request.data.get("email") or "").strip().lower()
        password = str(request.data.get("password") or "")

        if not username and not email:
            return Response({"detail": "username (or email) and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"detail": "username (or email) and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        login_username = username
        if not login_username and email:
            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            login_username = user_obj.username

        user = authenticate(request, username=login_username, password=password)
        if not user:
            return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)