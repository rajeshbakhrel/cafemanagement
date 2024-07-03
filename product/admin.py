from django.contrib import admin
from .models import ProductItem ,Menu,Order_Item,MenuItem,StockManagement,Bill
# Register your models here.



class Admin_Menu(admin.ModelAdmin):
    list_display = ['id','category_name','category_img']
admin.site.register(Menu,Admin_Menu)

class Admin_MenuItem(admin.ModelAdmin):
    list_display = ['id','menu','item_type','item_img']
admin.site.register(MenuItem,Admin_MenuItem)
class Admin_Item(admin.ModelAdmin):
    list_display = ['id', 'category','item_type','item_name','item_img','price']
admin.site.register(ProductItem,Admin_Item)



# class Admin_Tea_Item(admin.ModelAdmin):
#     list_display = ['id','black_tea','plane_milk_regular','zinger_milk_regular','cutting_half','cutting_full','matka_half','matka_full','lemon_water','description']


# admin.site.register(Tea_Item,Admin_Tea_Item)


class Admin_OrderItem(admin.ModelAdmin):
    list_display = ["id","img","table_no","category","item_type","product_items","quantity","total_price","get_order"]
admin.site.register(Order_Item,Admin_OrderItem)


class StockAdmin(admin.ModelAdmin):
        list_display = ["id","menu","menu_item","product_item","description","price","quantity","total_price"]
admin.site.register(StockManagement,StockAdmin)


# # @admin.register(Bill)
# class BillAdmin(admin.ModelAdmin):
#     list_display = ("id","table_no",'order_item',  'total_amount', 'paid_amount', 'created_at', 'updated_at')
# admin.site.register(Bill,BillAdmin)





class BillAdmin(admin.ModelAdmin):
    list_display = ('table_no', 'total_amount', 'payment_status', 'created_at')
    search_fields = ('table_no',)
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    list_filter = ('payment_status',)
    
    def save_model(self, request, obj, form, change):
        obj.total_amount = obj.order_item.total_price
        super().save_model(request, obj, form, change)

admin.site.register(Bill, BillAdmin)




    # def get_table_no(self, obj):
    #     return obj.order_item.table_no
    # get_table_no.short_description = 'Table No'
# class BillAdmin(admin.ModelAdmin):
#     list_display = ("id",'table_no', 'order_items','total_amount')
# admin.site.register(Bill,BillAdmin)

# class BillAdmin(admin.ModelAdmin):
#     list_display = ('table_no', 'total_amount',)
#     search_fields = ('table_no',)
#     readonly_fields = ('total_amount',)
#     filter_horizontal = ('order_items',)

#     def save_model(self, request, obj, form, change):
#         # Save the Bill object first to get the ID
#         super().save_model(request, obj, form, change)
#         # Then update the total_amount and save again
#         obj.total_amount = obj.calculate_total_amount()
#         obj.save()

# admin.site.register(Bill, BillAdmin)

# from django.contrib import admin
# from .models import Menu, Menu_Item, Product_Item, Order_Item

# class MenuAdmin(admin.ModelAdmin):
#     list_display = ['category_name']
#     search_fields = ['category_name']

# class Menu_ItemAdmin(admin.ModelAdmin):
#     list_display = ['item_type', 'menu']
#     list_filter = ['menu']
#     search_fields = ['item_type']

# class Product_ItemAdmin(admin.ModelAdmin):
#     list_display = ['item_name', 'category', 'item_type', 'price']
#     list_filter = ['category', 'item_type']
#     search_fields = ['item_name']

# class Order_ItemAdmin(admin.ModelAdmin):
#     list_display = ['product_items', 'table_no', 'quantity', 'get_order']
#     list_filter = ['table_no', 'category', 'item_type', 'get_order']
#     search_fields = ['product_items__item_name']

# admin.site.register(Menu, MenuAdmin)
# admin.site.register(Menu_Item, Menu_ItemAdmin)
# admin.site.register(Product_Item, Product_ItemAdmin)
# admin.site.register(Order_Item, Order_ItemAdmin)
