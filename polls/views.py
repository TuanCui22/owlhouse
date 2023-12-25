from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, CustomUser, Cart
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from django.db.models import Q
from django.http import HttpResponseRedirect

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                logout(request)
    else:
        form = RegistrationForm()

    return render(request, 'polls/register_index.html', {'form': form})

def forgot_pass_view(request):
    return render(request, 'polls/forgot_pass_index.html')

def homepage_view(request):
    feature_products = Product.objects.all()[:4]
    return render(request, 'polls/homepage_index.html', {'feature_products': feature_products})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Authentication successful
            user = form.get_user()
            login(request, user)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'polls/login_index.html', {'form': form})

@login_required
def cart_view(request):
    user = request.user
    list_item=[]
    cart = Cart.objects.filter(user=user)
    for c in cart:
        list_item.append(c.product_id)
    
    item = Product.objects.filter(
        id__in=list_item
    )
    return render(request, 'polls/shopping_cart_index.html', {'items': item, 'cart': cart})

def listbooks_view(request):
    products = Product.objects.all()
    return render(request, 'polls/list_book_index.html', {'products': products})

def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related_products = Product.objects.filter(category=product.category)[:4]
    return render(request, 'polls/onlybooks.html', {'product': product, 'related_products': related_products})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'polls/list_book_index.html', {'category': category,'products': products})

def search(request):
    search_product = request.GET.get('search')
    uppercase_product = str(search_product).upper()
    products = ''
    if search_product:
        products = Product.objects.filter(Q(title__icontains=uppercase_product) & Q(description__icontains=uppercase_product))
    else:
    # If not searched, return default posts
        products = ''
    if products:
        count = products.count()
    else:
        count = 0
    return render(request, 'polls/search_product.html', {'products': products, 'search_product': search_product, 'count': count})

@login_required
def add_cart(request, product_id, quantity):
    user = request.user
    cart = Cart.objects.filter(user=user, product_id=product_id)
    if request.POST.get('amount'):
        quantity = request.POST.get('amount')
        quantity = int(quantity)
        
    if cart.exists():
        existed_cart = Cart.objects.get(user=user, product_id=product_id)
        existed_cart.quantity += quantity
        existed_cart.save()
    else:
        new_cart = Cart.objects.create(user=user, product_id=product_id, quantity = 1)
    return redirect('http://127.0.0.1:8000')

@login_required
def update_from_cart(request, product_id, quantity):
    user = request.user
    cart = Cart.objects.get(user=user, product_id=product_id)
    
    quantity = int(quantity)
    cart.quantity = quantity
    cart.save()
    return redirect('http://127.0.0.1:8000')

@login_required
def remove_from_cart(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    if request.method == 'POST':
        cart.delete()
    return render(request, 'polls/shopping_cart_index.html')




@login_required
def account_view(request):
    return render(request, 'polls/account_view.html')

def payment_view(request):
    return render(request, 'polls/pay_index.html')