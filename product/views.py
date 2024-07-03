from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Menu_Serializer,Product_Item_Serializer,Order_Item_Serializer,MenuItem_serializer,StockManagementSerializer,BillSerializer,MenuItemSearch_Serializer
from .models import Menu , ProductItem,Order_Item,MenuItem,StockManagement,Bill
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.





class Menu_List(APIView):
    # Authentication = [AllowAny]

    def get(self,request):
       category = Menu.objects.all()
       serializer = Menu_Serializer(Menu,many = True)
       return Response(serializer.data)

    def post(self,request):
        serializer =Menu_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

class Menu_Detail(APIView):
    def get_object(self,pk):
        try:
            return Menu.objects.get(pk=pk )
        except Menu.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        category = self.get_object(pk)
        serializer = Menu_Serializer(Menu)
        return Response(serializer.data)

    def put(self,request,pk):
        category = self.get_object(pk)
        serializer = Menu_Serializer(category,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

class Menu_ItemList(APIView):
    serializer = MenuItemSearch_Serializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name','category','price']

    def get(self,request):
        item = MenuItem.objects.all()
        serializer = MenuItem_serializer(item,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        item = MenuItem.objects.all()
        serializer = MenuItem_serializer(data=request.data)
        return Response(serializer.data)

class Menu_ItemDetail(APIView):
    def get_object(self,request,pk):
        try:

          return MenuItem.objects.get(pk = pk)
        except MenuItem.DoesNotExist:
            return 404
        
    def get(self,request,pk):
        item = self.get_object(pk)
        serializer = MenuItem_serializer(item)
        return Response(serializer.data)
    
    
    def put(self,request,pk):
        item = self.get_object(pk)
        serializer = MenuItem_serializer(item,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    


        


class Product_ItemList(APIView):

    def get(self,request):
        product = ProductItem.objects.all()
        serializer = Product_Item_Serializer(product,many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = Product_Item_Serializer( data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    def filteritem(self,request):
        categories = Menu.objects.all()
        menu_item = MenuItem.objects.all()
        item = ProductItem.objects.all()
        items = ProductItem.objects.get(data = request.data)
        selected_category_id = request.GET.get('categories')
        if selected_category_id:
            try:
                category = Menu.objects.get(id = 'selected_category_id')
                menu_item = MenuItem.filter(category = category)
            except Menu.DoesNotExist:
                return HttpResponseBadRequest("Invalid category_id")
    
        return menu_item

class Product_ItemDetail(APIView):

    def get_object(self,pk):
        try:
            return ProductItem.objects.get(pk=pk)
        except ProductItem.DoesNotExist:
            return 404
    
    def get(self,request,pk):
        product = self.get_object(pk)
        serializer = Product_Item_Serializer(product)
        return Response(serializer.data)

    def put(self,request,pk):
        product = self.get_object(pk)
        serializer = Product_Item_Serializer(product,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = 400)
    
    def delete(self,request,pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
    
class Order_ItemView(APIView):

    def get(self,request):
        items = Order_Item.objects.all()
        serializer = Order_Item_Serializer(items,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = Order_Item_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Order_ItemDetail(APIView):

    def get_object(self,pk):
        try:
            items = Order_Item.objects.get(pk=pk)
            return items
        except Order_Item.DoesNotExist:
            return 404
    
    def get(self,request,pk):
        items = self.get_object(pk)
        serializer = Order_Item_Serializer(items)
        return Response(serializer.data)

    def put(self,request,pk):
        items = self.get_object(pk)
        serializer = Order_Item_Serializer(items,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        items = Order_Item.objects.get(id = pk)
        data = items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class Stock_List(APIView):
    def get(self,request):
        stock = StockManagement.objects.all()
        serializer = StockManagementSerializer(stock,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        # stock = StockManagement.objects.all()
        serializer = StockManagementSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class Stock_Detail(APIView):
    def get_object(self,request,pk):
        try:
            stock = StockManagement.objects.get(pk=pk)
            return stock

        except StockManagement.DoesNotExist:
            return 404
        
    def get(self,request,pk):
        stock = self.get_object(pk)
        serializer = StockManagementSerializer(stock)
        return Response(serializer.data)

    def put(self,request,pk):
        items = self.get_object(pk)
        serializer = StockManagementSerializer(items,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        items = StockManagement.objects.get(id = pk)
        data = items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class Bill_List(APIView):
#     def get(self,request):
#         bill = Bill.objects.all()
#         serializer = BillSerializer(bill,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         # stock = StockManagement.objects.all()
#         serializer = BillSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
# class Bill_Detail(APIView):
#     def get_object(self,request,pk):
#         try:
#             stock = Bill.objects.get(pk=pk)
#             return stock

#         except StockManagement.DoesNotExist:
#             return 404
        
#     def get(self,request,pk):
#         bill= self.get_object(pk)
#         serializer = BillSerializer(bill)
#         return Response(serializer.data)

#     def put(self,request,pk):
#         items = self.get_object(pk)
#         serializer = BillSerializer(items,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     def delete(self,request,pk):
#         items = Bill.objects.get(id = pk)
#         data = items.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    