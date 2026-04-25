"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from songgenerationrequest.views import (
    generate_ai_music_page,
    home_page,
    my_songs_page,
    sign_in_page,
    sign_up_page,
)

urlpatterns = [
    path("", home_page, name="home"),
    path("signin/", sign_in_page, name="signin"),
    path("signup/", sign_up_page, name="signup"),
    path("generate-ai-music/", generate_ai_music_page, name="generate_ai_music"),
    path("my-songs/", my_songs_page, name="my_songs"),
    path('admin/', admin.site.urls),
    path("api/song/", include("song.urls")),
    path("api/user/", include("user.urls")),
    path("api/song-generation-requests/", include("songgenerationrequest.urls")),
    path("api/sharelinks/", include("sharelink.urls")),
]
