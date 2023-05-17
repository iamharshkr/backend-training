from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Products
from .serializers import ProductSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    # return Response("Hello, world.")
    return render(request, 'home.html', {'name': 'John', "age": 45})


@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username', '')
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
    

@api_view(['GET', 'POST'])
def products(request, prod_id=None):
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
        products = Products.objects.create(name=name, price=price, stock=stock, image_url=image_url) # INSERT INTO products (name, price, stock, image_url) VALUES (name, price, stock, image_url);
        serializer = ProductSerializer(products)
        return Response(serializer.data)