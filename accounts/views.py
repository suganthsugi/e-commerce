from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from main.models import *

# Create your views here.


def signup(request):
    if(request.method == 'POST'):
        uname = request.POST['uname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if(pass1==pass2):
            if(not(User.objects.filter(username=uname).exists())):
                user = User.objects.create_user(uname, email, pass1)
                user.save()
                Customer.objects.create(user=User.objects.get(username=uname), name=uname, email=email)
                return redirect('/accounts/login/')
            else:
                msg={'err':f'Sorry! The username {uname} is alredy taken, Please try someothing else'}
                return render(request, 'error.html', msg)
        else:
            msg={'err':'The Password Dosen\'t matches'}
            return render(request, 'error.html', msg)
    else:
        context={}
        return render(request, 'signup.html', context)

def login(request):
    if(request.method=='POST'):
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        
        currentUser = auth.authenticate(username=uname, password=pass1)
        if(currentUser is not None):
            auth.login(request, currentUser)
            return redirect('/')
        else:
            msg={'err':f'The Username or Password is incorrect'}
            return render(request, 'usererr.html', msg)
        
    context={}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def detail(request):
    cus = Customer.objects.get(user=User.objects.get(username=request.user))
    if(ShippingAddress.objects.filter(customer=cus).exists()):
        address = ShippingAddress.objects.get(customer=cus)
        adds=f"{address.get('address')}, {address.get('city')}, {address.get('state')}, {address.get('zipcode')}"
    else:
        adds='Address will be updated once you order the product'
    context = {'cus':cus, 'address':adds}
    return render(request, 'detail.html', context)