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
        email = str(request.data.get("email") or "").strip().lower()
        password = str(request.data.get("password") or "")

        if not email or not password:
            return Response(
                {"detail": "email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response({"detail": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Django's AbstractUser still requires a unique username; generate one from email.
        base = (email.split("@")[0] or "user").strip()[:20] or "user"
        candidate = base
        i = 1
        while User.objects.filter(username=candidate).exists():
            i += 1
            suffix = f"{i}"
            candidate = (base[: (20 - len(suffix))] + suffix) if len(base) >= len(suffix) else (base + suffix)

        user = User.objects.create_user(username=candidate, email=email, password=password)
        serializer = UserSerializer(user)
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthSignInAPIView(APIView):
    def post(self, request):
        email = str(request.data.get("email") or "").strip().lower()
        password = str(request.data.get("password") or "")

        if not email or not password:
            return Response({"detail": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user_obj.username, password=password)
        if not user:
            return Response({"detail": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)