from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced

# Register your models here.
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name', 'locality' , 'city', 'state', 'zipcode']
    list_filter = ['id']
    search_fields = ["name__startswith"]

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price', 'discounted_price' , 'brand', 'category']
    list_filter = ['brand' ]
    search_fields = ["title__startswith"]

class CarttModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product', 'quantity' ]

class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product', 'quantity' ,'ordered_date']
    list_filter = ['ordered_date']

admin.site.register(Customer,CustomerModelAdmin)
admin.site.register(Product,ProductModelAdmin)
admin.site.register(Cart,CarttModelAdmin)
admin.site.register(OrderPlaced,OrderPlacedModelAdmin)
