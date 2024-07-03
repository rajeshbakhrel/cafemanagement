from rest_framework import serializers
from .models import Menu,ProductItem,Order_Item,MenuItem,StockManagement,Bill



class Menu_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields ='__all__'

    # def update(self,instance,validate_data):
    #         instance.category_name = validate_data.get('name',instance.category_name)
    #         # instance.description = validate_data.get('description',instance.description)

    #         instance.save()
    #         return instance

class MenuItem_serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemSearch_Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class Product_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'

class ProductItemsearch_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'

# class Tea_Item_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tea_Item
#         fields = '__all__'         

class Order_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Item
        fields = ('id','img','table_no','cate','items','quantity','get_order')
        depth = 2

class StockManagementSerializer(serializers.Serializer):
    class Meta:
        model = StockManagement
        fields = '__all__'


class BillSerializer(serializers.Serializer):
    class Meta:
        model = Bill
        fields = '__all__'