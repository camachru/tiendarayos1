
from django.contrib import admin
from io import open

from .models import (
    Product, 
    Order, 
    OrderItem, 
    ColourVariation,
    SizeVariation,
    Address,
    Payment,
    Category,
    addresses,
    
    
)

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AddressResource(resources.ModelResource):
    class Meta:
        model = Address

class addressesResource(resources.ModelResource):
    class Meta:
        model = addresses

class addressesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        search_fields = ['d_codigo']
        list_display = [ 
            'd_codigo',
        ]
        resource_class = addressesResource

class AddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['zip_code']
    list_display = (
        'zip_code',
        'address_type',)
    
    resource_class = AddressResource


admin.site.register(Product)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColourVariation)
admin.site.register(SizeVariation)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(addresses, addressesAdmin)
