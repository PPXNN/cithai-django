from django.shortcuts import render

# Create your views here.
def search_user(request):
    return render(request, "user/search-user.html")
