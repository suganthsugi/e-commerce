from django.contrib import admin
from main.models import *

# Register your models here.

class ContentAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/blog.css',)
        }
        js = ('js/blog.js',)

admin.site.register(Customer)
admin.site.register(Product, ContentAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(OrderItem)