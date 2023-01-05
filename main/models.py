from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    isadmin = models.BooleanField(default=False)
    ismoderator = models.BooleanField(default=False)
    isnormaluser = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = (
        ('all','all'),
        ('mobile','mobile'),
        ('laptop','laptop'),
        ('watch','watch'),
        ('accessory','accessory'),
    )
    product_catogory = (
        ('all','all'),
        ('mobile','mobile'),
        ('earphone','earphone'),
        ('keyboard','keyboard'),
        ('mouse','mouse'),
        ('headset','headset'),
        ('laptop','laptop'),
        ('pc','pc'),
        ('mobile-case','mobile-case'),
        ('laptop-case','laptop-case'),
        ('ladies-watch','ladies-watch'),
        ('mens-watch','mens-watch'),
        ('camera','camera'),
        ('mobile-accessory','mobile-accessory'),
        ('speaker','speaker'),
        ('laptop-accessory','laptop-accessory'),
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    desc=models.TextField(null=True, blank=True)
    category=models.CharField(choices=category, max_length=70, default='all')
    product_catogory=models.CharField(choices=product_catogory, max_length=70, default='all')
    image=models.ImageField(null=True , blank=True, upload_to='images',default='default.png')
    product_avail = models.BooleanField( default = True)
    sponsered = models.BooleanField( default = False)
    detail=models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True, blank=True)
    date_of_feedback = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product}, {self.customer}'


class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    date_orderd=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False )
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping

    @property
    def get_cart_total(self):
        orderitems= self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems= self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0, null=True,blank=True)
    date_added =models.DateTimeField(auto_now_add=True) 

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True) 
    city=models.CharField(max_length=200,null=True) 
    state=models.CharField(max_length=200,null=True) 
    zipcode=models.CharField(max_length=200,null=True)
    date_added =models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return self.address