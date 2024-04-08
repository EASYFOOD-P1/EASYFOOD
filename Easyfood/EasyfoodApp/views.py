from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def products(request):
    query = request.GET.get('searchProduct')
    results = None

    if query:
        results = Product.objects.filter(title__icontains=query)
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'results': results})

def login(request):
    return render(request, 'login.html')
