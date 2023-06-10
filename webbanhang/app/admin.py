from django.contrib import admin
from .models import *

class  authorAdmin(admin.ModelAdmin):
    list_display=('customer','product','order','quantity','date_added')
    list_foreign_key_links = ('customer',)
    list_filter = (
        ('order', admin.RelatedFieldListFilter),
    )
          
    def temp(self,obj):
        print(obj.customer)
        return 1
class shipping(admin.ModelAdmin):
    list_display = ('customer','order')
    list_foreign_key_links = ('customer',)
    list_filter = (
        ('order', admin.RelatedFieldListFilter),
    )

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem,authorAdmin)
admin.site.register(ShippingAddress,shipping)