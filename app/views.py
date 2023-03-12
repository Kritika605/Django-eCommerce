from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.views import View
from .forms import CustomerRegitrationForm ,LoginForm, CustomerProfileForm
from .models import Customer,Product,Cart, OrderPlaced
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

# Create your views here.
# def home(request):
#     return render(request,"app/home.html")

class ProductView(View):
    def get(self,request):
        women_cloths = Product.objects.filter(Q(category = 'WTW')|Q(category = 'WBW'))
        men_cloths = Product.objects.filter(Q(category = 'MTW')|Q(category = 'MBW'))
        
        context = {
            'women_cloths':women_cloths,
            'men_cloths' :men_cloths,
        }
        return render(request,"app/home.html",context)

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk = pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
        context = {
            'product': product,
            'item_already_in_cart' : item_already_in_cart
        }
        return render(request,"app/product_detail.html",context)

class SearchView(View):
    def get(self,request):
        query = request.GET.get('search')
        if query :
            products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query) )
        else:
            products = None
        return render(request, 'app/productlist.html', {'products': products})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegitrationForm()
        return render(request,"app/registration.html",{'form':form})

    def post(self,request):
        form = CustomerRegitrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Registered Successfully.')
        return render(request,"app/registration.html",{'form':form})


def resetpassword(request):
    return render(request,"app/resetpassword.html")

@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"app/profile.html",{'form':form})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr =  request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state =form.cleaned_data['state']
            zipcode =  form.cleaned_data['zipcode']          
            cust = Customer(user = usr,name =name, locality= locality,city = city,state=state ,zipcode = zipcode )
            cust.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        return render(request,"app/profile.html",{'form':form})

@method_decorator(login_required, name='dispatch')
class OrdersView(View):
    def get(self,request):
        orders = OrderPlaced.objects.filter(user = request.user)
        context = {
            'orders' : orders
        }
        return render(request,"app/orders.html",context)

@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self,request):
        address = Customer.objects.filter(user=request.user)
        return render(request,"app/address.html",{'address':address})

class MobileView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'M')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

class LaptopView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'L')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

class MenTopWearView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'MTW')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

class MenBottomWearView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'MBW')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

class WomenTopWearView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'WTW')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

class WomenBottomWearView(View): 
    def get(self,request):
        products = Product.objects.filter(category = 'WBW')
        context = {
            'products':products,
        }
        return render(request,"app/productlist.html",context)

@method_decorator(login_required, name='dispatch')
class Add_to_cart(View):
    def get(self,request):
        if request.user.is_authenticated:
            product_id = request.GET.get('prod_id')
            product = Product.objects.get(id = product_id)
            Cart(user=request.user, product= product,quantity=1).save()
            return HttpResponseRedirect(reverse("product_detail", args=(product_id,)))

@method_decorator(login_required, name='dispatch')
class ShowCart(View):
    def get(self,request):
        carts = Cart.objects.filter(user = request.user)
        amount = 0.0
        shipping_charge = 70.0
        prod_list = [c for c in Cart.objects.all() if c.user == request.user]
        if prod_list:
            for prod in prod_list:
                tempamount = prod.quantity * prod.product.discounted_price
                amount = amount + tempamount  
                cart_total = amount 
            context = {
                'amount' : amount,
                'shipping_charge' : shipping_charge,
                'cart_total' : cart_total + shipping_charge,
                'carts' : carts
            }
            return render(request,"app/show_cart.html",context)
        return render(request,'app/emptycart.html')

def pluscart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id") 
        cart_prod = Cart.objects.get(Q(product = prod_id) & Q(user = request.user) )
        cart_prod.quantity +=1
        cart_prod.save()
        amount = 0.0
        shipping_charge = 70.0
        prod_list = [c for c in Cart.objects.all() if c.user == request.user]
        for prod in prod_list:
            prod_totalamount =( prod.quantity * prod.product.discounted_price)
            amount = amount + prod_totalamount
            cart_total = amount

        context = {
            'quantity' : cart_prod.quantity,
            'amount' : amount,
            'shipping_charge' : shipping_charge,
            'cart_total' : cart_total + shipping_charge,
        }
        return JsonResponse(context)

def minuscart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id") 
        cart_prod = Cart.objects.get(Q(product = prod_id) & Q(user = request.user) )
        cart_prod.quantity -=1
        cart_prod.save()
        amount = 0.0
        shipping_charge = 70.0
        prod_list = [c for c in Cart.objects.all() if c.user == request.user]
        for prod in prod_list:
            prod_totalamount =( prod.quantity * prod.product.discounted_price)
            amount = amount + prod_totalamount
            cart_total = amount 

        context = {
            'quantity' : cart_prod.quantity,
            'amount' : amount,
            'shipping_charge' : shipping_charge,
            'cart_total' : cart_total + shipping_charge,
        }
        return JsonResponse(context)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id") 
        cart_prod = Cart.objects.get(Q(product = prod_id) & Q(user = request.user) )
        cart_prod.delete()
        amount = 0.0
        shipping_charge = 70.0
        prod_list = [c for c in Cart.objects.all() if c.user == request.user]
        for prod in prod_list:
            prod_totalamount =( prod.quantity * prod.product.discounted_price)
            amount = amount + prod_totalamount
            cart_total = amount 

        context = {
            'amount' : amount,
            'shipping_charge' : shipping_charge,
            'cart_total' : cart_total + shipping_charge,
        }
        return JsonResponse(context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        product = Product.objects.get(id = prod_id)
        Cart(user=request.user, product= product,quantity=1).save()

        cart_prod =   Cart.objects.filter(user = request.user) 
        address = Customer.objects.filter(user = request.user)
        amount = 0.0
        shipping_charge = 70.0
        prod_list = [c for c in Cart.objects.all() if c.user == request.user]
        for prod in prod_list:
            prod_totalamount =( prod.quantity * prod.product.discounted_price)
            prod_discountamount =prod_totalamount-( prod.quantity * prod.product.selling_price)
            amount = amount + prod_totalamount
        context = {
            'cart_prod' : cart_prod,
            'address' : address,
            'prod_totalamount' : prod_totalamount,
            'amount': amount,
            'total_amount' : amount+shipping_charge,
            'shipping_charge' :shipping_charge,
            'prod_discountamount' : prod_discountamount
        }
        return render(request,'app/placeorder.html',context)

def payment_done(request):
    user = request.user
    cust_id = request.GET.get("custid")
    customer = Customer.objects.get(id = cust_id)
    cart_prod = Cart.objects.filter(user= user)
    for c in cart_prod:
        OrderPlaced(user = user, customer = customer, product = c.product, quantity = c.quantity).save()
        c.delete()
    return redirect('orders')




    