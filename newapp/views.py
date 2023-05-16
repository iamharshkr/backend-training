from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET'])
def index(request):
    # return Response("Hello, world.")
    return render(request, 'home.html', {'name': 'John'})


@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        return render(request, 'dashboard.html',{'name': username})
    if request.method == 'GET':
        return render(request, "login.html")
    
@api_view(['GET'])
def dashboard(request):
    if request.user.is_authenticated:
        name = request.GET.get('name')
        return render(request, 'dashboard.html', {'name': name})
    else:
        return render(request, 'login.html', {"error": "You are not logged in"})