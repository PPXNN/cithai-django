from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponse
from django.utils.crypto import get_random_string
import requests
import json
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


class AuthSignOutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "signed out"}, status=status.HTTP_200_OK)


class AuthMeAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthGoogleAPIView(APIView):
    @staticmethod
    def _resolve_google_user(id_token: str):
        google_client_id = str(getattr(settings, "GOOGLE_CLIENT_ID", "") or "").strip()
        if not google_client_id:
            return None, "GOOGLE_CLIENT_ID is not configured", status.HTTP_500_INTERNAL_SERVER_ERROR, False

        try:
            google_resp = requests.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": id_token},
                timeout=10,
            )
        except requests.RequestException:
            return None, "google verification failed", status.HTTP_502_BAD_GATEWAY, False

        if google_resp.status_code != 200:
            return None, "invalid google token", status.HTTP_401_UNAUTHORIZED, False

        token_data = google_resp.json()
        if token_data.get("aud") != google_client_id:
            return None, "google token audience mismatch", status.HTTP_401_UNAUTHORIZED, False

        email = str(token_data.get("email") or "").strip().lower()
        if not email:
            return None, "google account email is required", status.HTTP_400_BAD_REQUEST, False

        if token_data.get("email_verified") not in ("true", True):
            return None, "google email is not verified", status.HTTP_401_UNAUTHORIZED, False

        user = User.objects.filter(email=email).first()
        created = False
        if not user:
            preferred_username = (token_data.get("name") or email.split("@")[0] or "google_user").strip()
            base_username = preferred_username.replace(" ", "_")
            username = base_username
            suffix = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{suffix}"
                suffix += 1

            first_name = str(token_data.get("given_name") or "").strip()
            last_name = str(token_data.get("family_name") or "").strip()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=get_random_string(32),
                first_name=first_name,
                last_name=last_name,
                auth_provider=User.AuthProvider.GOOGLE,
            )
            created = True
        elif user.auth_provider == User.AuthProvider.LOCAL:
            user.auth_provider = User.AuthProvider.GOOGLE
            user.save(update_fields=["auth_provider"])

        return user, "", status.HTTP_201_CREATED if created else status.HTTP_200_OK, created

    def post(self, request):
        google_id_token = str(request.data.get("id_token") or "").strip()
        if not google_id_token:
            return Response({"detail": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, error_message, http_status, _ = self._resolve_google_user(google_id_token)
        if not user:
            return Response({"detail": error_message}, status=http_status)

        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=http_status)


class AuthGoogleRedirectAPIView(AuthGoogleAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        google_id_token = str(request.POST.get("credential") or "").strip()
        if not google_id_token:
            return HttpResponse(
                "<script>window.location.href='/signin/?google_error=missing_credential';</script>",
                status=400,
            )

        user, error_message, _, _ = self._resolve_google_user(google_id_token)
        if not user:
            error_value = json.dumps(error_message)
            return HttpResponse(
                f"<script>window.location.href='/signin/?google_error=' + encodeURIComponent({error_value});</script>",
                status=401,
            )

        login(request, user)
        user_payload = json.dumps(UserSerializer(user).data)
        return HttpResponse(
            "<script>"
            f"localStorage.setItem('currentUser', JSON.stringify({user_payload}));"
            "window.location.href='/generate-ai-music/';"
            "</script>"
        )