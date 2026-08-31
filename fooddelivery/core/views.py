
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import FoodItem, Order, CartItem
from .forms import RegisterForm

def home(request):
    items = FoodItem.objects.all()
    return render(request, 'home.html', {'items': items})

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    item = get_object_or_404(FoodItem, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        total = sum(item.total_price() for item in cart_items)
        order = Order.objects.create(user=request.user, total_amount=total)
        for c_item in cart_items:
            order.items.add(c_item.item)
        cart_items.delete()
    return redirect('my_orders')

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')