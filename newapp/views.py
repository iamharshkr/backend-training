from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Products
from .serializers import ProductSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
@api_view(['GET'])
def index(request):
    # return Response("Hello, world.")
    return render(request, 'home.html', {'name': 'John', "age": 45})


@api_view(['POST'])
def login(request):
    try:
        if request.method == 'POST':
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                serializer = UserSerializer(user)
                #user = User.objects.get(username=username, password=password) wrong
                return Response({"user": serializer.data,"access_token": access_token, "refresh_token": str(refresh)})
            else:
                return Response({"error": "Wrong credentials"})
    except Exception as e:
        return Response({"error": str(e)})

@api_view(['GET'])
def dashboard(request):
    if request.user.is_authenticated:
        name = request.GET.get('name')
        return render(request, 'dashboard.html', {'name': name})
    else:
        return render(request, 'login.html', {"error": "You are not logged in"})
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def products(request, prod_id=None):
    try:
        if request.method == 'GET':
            products = Products.objects.all() # SELECT * FROM products;
            if prod_id:
                products = products.filter(id=prod_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            name = request.data.get('name')
            price = request.data.get('price')
            stock = request.data.get('stock')
            image_url = request.data.get('image_url')
            description = request.data.get('description')
            products = Products.objects.create(name=name, price=price, stock=stock, image_url=image_url, description=description) # INSERT INTO products (name, price, stock, image_url) VALUES (name, price, stock, image_url);
            serializer = ProductSerializer(products)
            return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)})


@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)