from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from canteen.models import FoodItem
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Cart, Orders, OrderItems
from .forms import LoginRegisterForm
import random
from django.http import JsonResponse
from django.urls import reverse
import re
# Create your views here.
def index(request):
    food = FoodItem.objects.all()
    name_quantity_of_all_food = []
    if(request.user.is_authenticated):
        cartitems = Cart.objects.filter(username=request.user)
        for f in food:
            find = False
            name_quantity_combo = []
            for item in cartitems:
                if(f.name == item.food.name):
                    name_quantity_combo.append(f.name)
                    name_quantity_combo.append(item.quantity)
                    find = True
                    break
            if(not find):
                name_quantity_combo.append(f.name)
                name_quantity_combo.append('0')
            name_quantity_of_all_food.append(name_quantity_combo)
    return render(request, 'order/index.html', {'food':food, 'cartitems':name_quantity_of_all_food})

def register(request):
    if(request.method == 'GET'):
        form = LoginRegisterForm()
        return render(request, 'order/register.html', {'form':form})
    elif(request.method == 'POST'):
        form = LoginRegisterForm(request.POST)
        un = request.POST.get('username')
        pw = request.POST.get('password')
        email = request.POST.get('email')
        if(User.objects.filter(username=un).exists()):
            messages.warning(request, 'User Already Exists, try other unique username')
            return HttpResponseRedirect('/register/')
        else:
            if(form.is_valid()):
                un = form.cleaned_data['username']
                pw = form.cleaned_data['password']
                mail = form.cleaned_data['email']
                new_user = User(username=un,email=email)
                new_user.set_password(pw)
                new_user.save()
                messages.success(request, 'Account Created Successfully, You can Login Now')
                return HttpResponseRedirect('/login/')

def user_login(request):
    if(request.method == 'GET'):
        form = LoginRegisterForm()
        return render(request, 'order/login.html', {'form':form})
    elif(request.method == 'POST'):
        form = LoginRegisterForm(request.POST)
        un = request.POST.get('username')
        pw = request.POST.get('password')
        email = request.POST.get('email')
        if(not User.objects.filter(username=un).exists()):
            messages.warning(request, 'User Does Not Exist or Wrong Password, Try Again')
            return HttpResponseRedirect('/login/')
        else:
            auth_user = authenticate(username=un, password=pw)
            if(auth_user):
                login(request, auth_user)
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, 'User Does Not Exist or Wrong Password, Try Again')
                return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def update_cart(request, f_id):
    food = FoodItem.objects.get(id=f_id)
    if(Cart.objects.filter(username=request.user, food=food).exists()):
        old_quantity = Cart.objects.values_list('quantity', flat=True).get(username=request.user, food=food)
        if(request.GET.get('name') == 'increase_cart'):
            updated_quantity = old_quantity + 1
            Cart.objects.filter(username=request.user, food=food).update(quantity=updated_quantity)
        elif(request.GET.get('name') == 'decrease_cart'):
            updated_quantity = old_quantity - 1
            Cart.objects.filter(username=request.user, food=food).update(quantity=updated_quantity)
        elif(request.GET.get('name') == 'delete_cart_item'):
            item_to_delete = Cart.objects.get(username=request.user, food=food)
            item_to_delete.delete()
    else:
        cart_item = Cart(username=request.user, food=food)
        cart_item.save()
    from_search = request.GET.get('from_search', 'False')
    if from_search == 'True':
        # return HttpResponseRedirect('/search_results/?q=' + request.GET['q'])
        query = request.GET.get('q', '')
    
        if query:
            # Search in both FoodItem name and description fields
            results = FoodItem.objects.filter(Q(name__icontains=query) | Q(restaurant__icontains=query))
        else:
            results = FoodItem.objects.all()
        
        name_quantity_of_all_food = []
        if request.user.is_authenticated:
            cartitems = Cart.objects.filter(username=request.user)
            for f in results:
                find = False
                name_quantity_combo = []
                for item in cartitems:
                    if f.name == item.food.name:
                        name_quantity_combo.append(f.name)
                        name_quantity_combo.append(item.quantity)
                        find = True
                        break
                if not find:
                    name_quantity_combo.append(f.name)
                    name_quantity_combo.append('0')
                name_quantity_of_all_food.append(name_quantity_combo)

        return render(request, 'order/search_results.html', {'query': query, 'results': results, 'cartitems': name_quantity_of_all_food})
    elif 'cart' in request.META.get('HTTP_REFERER', ''):
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')
            

@login_required(login_url='/login/')
def cart(request):
    cartitems = Cart.objects.filter(username=request.user)
    total_amount = 0
    if(cartitems):
        for item in cartitems:
            sub_total = item.food.price * item.quantity
            total_amount += sub_total
    return render(request, 'order/cart.html', {'cartitems':cartitems, 'total_amount':total_amount})

@login_required(login_url='/login/')
def checkout(request):
    if(request.method == 'POST'):
        if(request.POST.get('paymode') == 'Cash'):
            tn_id = 'CASH' + str(random.randint(111111111111111,999999999999999))
            payment_mode = "Cash"
            payment_gateway = "Cash"
        elif(request.POST.get('paymode') == 'Online' and request.POST.get('paygate') == "Paypal"):
            tn_id = request.POST.get('tn_id')
            payment_mode = "Online"
            payment_gateway = "Paypal"
        else:
            return HttpResponse('<H1>Invalid Request</H1>')
        cartitems = Cart.objects.filter(username=request.user)
        total_amount = 0
        new_order = Orders(username=request.user, total_amount=total_amount, payment_mode=payment_mode, transaction_id=tn_id, payment_gateway=payment_gateway)
        new_order.save()

        print(request.user.username)
        subject = 'Welcome to Your Canteen Ordering System'
        message = f'Thank you for registering, {request.user.username}!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        print("sending mail")
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("mail sent")

        
        if(cartitems):
            for item in cartitems:
                OrderItems(username=request.user, order=new_order, name=item.food.name, price=item.food.price, quantity=item.quantity, item_total=item.food.price * item.quantity).save()
                sub_total = item.food.price * item.quantity
                total_amount += sub_total
            Orders.objects.filter(id=new_order.id).update(total_amount=total_amount)
        cartitems.delete()
        return HttpResponseRedirect('/myorders/')
    else:
        return HttpResponse('<H1>Invalid Request</H1>')

@login_required(login_url='/login/')
def my_orders(request):
    orders = Orders.objects.filter(username = request.user).order_by("-order_datetime", "id")
    order_items = OrderItems.objects.filter(username = request.user)
    return render(request, 'order/myorders.html', {'orders':orders, 'order_items':order_items})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return HttpResponseRedirect('/')

def delivery_agent(request):
    username_pattern = r'^delivery_.*$'
    if re.match(username_pattern, request.user.username):
        if request.method == 'POST':
            # Handle form submission for updating delivery status
            order_id = request.POST.get('order_id')
            order = Orders.objects.get(id=order_id)
            # order = Orders.objects.filter(username=order_id)
            order.status = 'Delivered'
            order.save()
            orders = Orders.objects.filter(status='Pending')  # Assuming delivery agent is authenticated and assigned to orders
            return render(request, 'order/delivery_agent.html', {'orders': orders})

        # Fetch orders for the delivery agent
        orders = Orders.objects.filter(status='Pending')  # Assuming delivery agent is authenticated and assigned to orders
        return render(request, 'order/delivery_agent.html', {'orders': orders})
    else:
        # Redirect to a different page or show an error message
        return HttpResponse('<H1>Invalid Request</H1>')

def search_results(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search in both FoodItem name and description fields
        results = FoodItem.objects.filter(Q(name__icontains=query) | Q(restaurant__icontains=query))
    else:
        results = FoodItem.objects.all()
    
    name_quantity_of_all_food = []
    if request.user.is_authenticated:
        cartitems = Cart.objects.filter(username=request.user)
        for f in results:
            find = False
            name_quantity_combo = []
            for item in cartitems:
                if f.name == item.food.name:
                    name_quantity_combo.append(f.name)
                    name_quantity_combo.append(item.quantity)
                    find = True
                    break
            if not find:
                name_quantity_combo.append(f.name)
                name_quantity_combo.append('0')
            name_quantity_of_all_food.append(name_quantity_combo)

    return render(request, 'order/search_results.html', {'query': query, 'results': results, 'cartitems': name_quantity_of_all_food})

    # return render(request, 'order/search_results.html', {'query': query, 'results': results})
        
