from django.contrib import admin
from .models import CustomUser, Category, Product, Cart, Order, OrderItem

admin.site.register(CustomUser)
admin.site.register(Cart)
#admin.site.register(Order)
#admin.site.register(OrderItem)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'name', 'phone_num', 'address', 'date_order', 'paid']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'date_added']