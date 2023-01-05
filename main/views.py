from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from main.models import *


# Create your views here.


def home(request):
    if(request.user.is_authenticated):
        customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        products = reversed(Product.objects.all())
        context={'products':products, 'cartItems':cartItems}
    
    products = reversed(Product.objects.all())
    context={'products':products}
    return render(request, 'index.html', context);
     

def product(request, category):
	if(category!='all'):
		products = Product.objects.filter(category=category)
		context={'products':products, 'title':category}
		return render(request, 'product.html', context)
	else:
		products = Product.objects.filter(category='accessory')
		products = (products | Product.objects.filter(category='watch'))
		products = (products | Product.objects.filter(category='laptop'))
		products = (products | Product.objects.filter(category='mobile'))
		# products += Product.objects.filter(category='watch')
		# products += Product.objects.filter(category='accessory')
		context={'products':products, 'title':category}
		return render(request, 'product.html', context)
	# else:
	# 	products = Product.objects.filter(category='accessory', category='mobile', category='laptop', category='watch')
	# 	context={'products':products}
	# 	return render(request, 'product.html', context)

def prodetail(request, id):
    product=Product.objects.get(id=id)
    context={'product':product}
    return render(request, 'prodetail.html', context)


def cart(request):

	if request.user.is_authenticated:
		customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)



def checkout(request):
	if request.user.is_authenticated:
		customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)

def confirmOrder(request):
    if(request.method=='POST'):
        customer = Customer.objects.get(user=User.objects.get(username=request.user.username))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        tot=0
        for x in items:
            tot+=x.product.price*x.quantity
        return redirect('/')
 
def find(request):
    if(request.method=="POST"):
        term=request.POST['term']
        term=term.replace(' ', '')
        if(term=='menswatch' or term=='mens watch' or term=='men watch'):
            term='mens-watch'
        if(term=='womenswatch' or term=='womens watch' or term=='women watch' or term=='ladieswatch' or term=='ladies watch' or term=='ladies watch'):
            term='ladies-watch'
        if(term[-1]=='s'):
            term=term[:len(term)-1]
        if(Product.objects.filter(product_catogory=term).exists()):
            products=Product.objects.filter(product_catogory=term)
            context={'products':products}
            return render(request, 'product.html', context)
        else:
            products=Product.objects.all()
            err=f'Products for {term} not found'
            context={'products':products, 'err':err}
            return render(request, 'product.html', context)


def sell(request):
    context = {}
    return render(request, 'sellprod.html', context)