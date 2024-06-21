
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Cart,Order
from django.db.models import Q
import random
from django.db import transaction
from .forms import PaymentForm, AddressForm
from django.contrib.auth.decorators import login_required






def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect('login')
    else:
        return render(request,'register.html')


def contact(request):
    return render(request, 'contact.html')



def loginuser(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
           # auth.login(request,user)
           auth_login(request, user)

           return redirect('home')
        else:

            return render(request, 'errorpage.html')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['Products']=p
    return render(request,'index.html',context)


def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    context['Products']=p
    # print(p)
    return render(request,'index.html',context)


def sort(request,sv):
    print(type(sv))
    if sv == "0":
        col="-pcost"
    else:
        col="pcost"
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context["Products"]=p
    return render(request,"index.html",context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(pcost__gte=min)
    q2=Q(pcost__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context["Products"]=p
    return render(request,'index.html',context)

def product_details(request,pid):
    context={}
    context["Products"]=Product.objects.filter(id=pid)
    return render(request,"pdetails.html",context)




def addtocart(request, pid):
    # if request.user.is_authenticated:
    #     userid = request.user.id
    #     u = User.objects.filter(id=userid)
    #     print(u)
    #     p = Product.objects.filter(id=pid)
    #     print(p)
    #     c = Cart.objects.create(uid=u[0], pid=p[0])
    #     # c = Cart.objects.create(uid=u[0], pid=p)
    #     c.save()
    #     return render(request, 'added.html')
    # else:
    #     return redirect("/login")

    if request.user.is_authenticated:
        userid = request.user.id
        try:
            u = User.objects.get(id=userid)  # Get the User instance
            p = Product.objects.get(id=pid)  # Get the Product instance
            c = Cart.objects.create(uid=u, pid=p)  # Create the Cart object
            return render(request, 'added.html')
        except User.DoesNotExist:
            return redirect("/login")
        except Product.DoesNotExist:
            # Handle case where Product with given id doesn't exist
            return redirect("/some-error-page")
    else:
        return redirect("/login")



def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")








def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np =len(c)    #no of products
    for x in c:
        s=s+x.pid.pcost*x.qty
    context={}
    context['n']=np
    context['Products']=c
    context['total']=s
    return render(request,"viewcart.html",context)

def updateqty(request,qv,cid):
    #print(type(qv))
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart  ")



@login_required
@transaction.atomic
def placeorder(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if address_form.is_valid() and payment_form.is_valid():
            card_number = payment_form.cleaned_data['card_number']
            card_holder = payment_form.cleaned_data['card_holder']
            expiry_date = payment_form.cleaned_data['expiry_date']
            cvv = payment_form.cleaned_data['cvv']
            amount = payment_form.cleaned_data['amount']

            if card_number == '1234567812345678' and cvv == '123':
                try:
                    with transaction.atomic():
                        userid = request.user.id
                        cart_items = Cart.objects.filter(uid=userid)
                        if not cart_items:
                            return HttpResponse("Your cart is empty.")

                        address = address_form.save(commit=False)
                        address.user = request.user
                        address.save()

                        oid = random.randrange(1000, 9999)
                        total_cost = 0
                        ordered_items = []

                        for cart_item in cart_items:
                            Order.objects.create(
                                order_id=oid,
                                pid=cart_item.pid,
                                uid=cart_item.uid,
                                qty=cart_item.qty,
                                address=address  # Add address to order
                            )
                            total_cost += cart_item.pid.pcost * cart_item.qty
                            ordered_items.append(cart_item.pid)
                            cart_item.delete()

                        context = {
                            'Products': ordered_items,
                            'total': total_cost,
                            'n': len(ordered_items)
                        }
                        payment_form.save()
                        return render(request, 'payment_success.html', {'amount': amount})

                except Exception as e:
                    logger.error(f"Error occurred while placing order: {str(e)}")
                    return HttpResponse(f"Error occurred while placing order: {str(e)}")
            else:
                return render(request, 'payment_failed.html')
        else:
            return render(request, 'process_payment.html', {'payment_form': payment_form, 'address_form': address_form})
    else:
        address_form = AddressForm()
        payment_form = PaymentForm()
        return render(request, 'process_payment.html', {'payment_form': payment_form, 'address_form': address_form})



@login_required
def makepayment(request):
    # Calculate the total amount from the cart
    cart_items = Cart.objects.filter(uid=request.user)
    total_amount = sum(item.pid.pcost * item.qty for item in cart_items)

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST, initial={'amount': total_amount})
        if address_form.is_valid() and payment_form.is_valid():
            card_number = payment_form.cleaned_data['card_number']
            card_holder = payment_form.cleaned_data['card_holder']
            expiry_date = payment_form.cleaned_data['expiry_date']
            cvv = payment_form.cleaned_data['cvv']
            amount = payment_form.cleaned_data['amount']

            if card_number == '1234567812345678' and cvv == '123':
                try:
                    with transaction.atomic():
                        userid = request.user.id
                        cart_items = Cart.objects.filter(uid=userid)
                        if not cart_items:
                            return HttpResponse("Your cart is empty.")

                        address = address_form.save(commit=False)
                        address.user = request.user
                        address.save()

                        oid = random.randrange(1000, 9999)
                        total_cost = 0
                        ordered_items = []

                        for cart_item in cart_items:
                            Order.objects.create(
                                order_id=oid,
                                pid=cart_item.pid,
                                uid=cart_item.uid,
                                qty=cart_item.qty,
                                address=address
                            )
                            total_cost += cart_item.pid.pcost * cart_item.qty
                            ordered_items.append(cart_item.pid)
                            cart_item.delete()

                        context = {
                            'Products': ordered_items,
                            'total': total_cost,
                            'n': len(ordered_items)
                        }
                        payment_form.save()
                        return render(request, 'payment_success.html', {'amount': amount})

                except Exception as e:
                    return HttpResponse(f"Error occurred while placing order: {str(e)}")
            else:
                return render(request, 'payment_failed.html')
        else:
            return render(request, 'process_payment.html', {'payment_form': payment_form, 'address_form': address_form, 'total_amount': total_amount})
    else:
        address_form = AddressForm()
        payment_form = PaymentForm(initial={'amount': total_amount})
        return render(request, 'process_payment.html', {'payment_form': payment_form, 'address_form': address_form, 'total_amount': total_amount})

def about(request):
    return render(request,'aboutus.html')

def contact(request):
    return render(request,'contact.html')

def indexpage(request):
    return render(request,"index.html")


def blog(request):
    return render(request,"blog.html")

def filtercat(request):
    return render(request,"filter.html")


def footer(request):
    return render(request,'footer.html')

# Create your views here.
def front(request):
    return render(request,"front.html")