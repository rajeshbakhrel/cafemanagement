from django.db import models
from django.core.exceptions import ValidationError
import os


from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


def img_upload_path(self,filename):
    return os.path.join('media',filename)


def validate_img(value):
    allowed_extensions = ['.png','.jpeg','.jpg']
    file_extension = value.name.split('.')[-1].lower()
    if '.'  + file_extension not in allowed_extensions:
        raise  ValidationError(f"only {allowed_extensions} are allowed")






class Menu(models.Model):
    # category_id is automatically created as the primary key
    category_name = models.CharField(max_length=255)
    category_img = models.ImageField(upload_to=img_upload_path, validators=[validate_img], blank=True, null=True)

    def __str__(self):
        return self.category_name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=255, blank=True, null=True)
    item_img = models.ImageField(upload_to=img_upload_path, validators=[validate_img], blank=True, null=True)

    def __str__(self):
        return self.item_type

class ProductItem(models.Model):
    category = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_type = models.ForeignKey(MenuItem, on_delete=models.CASCADE,blank=True,null=True)
    item_name = models.CharField(max_length=255)
    item_img = models.ImageField(upload_to=img_upload_path, validators=[validate_img], blank=True, null=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item_name} - {self.price} NRS"

    # def save(self,*args,**kwargs):
    #     self.item_type = self.filter_by_category()
    #     super().save(*args,**kwargs)

    # def filter_by_category(self,request):
    #     categ = self.category.objects.all()
    #     # type_filter = self.item_type.objects.all()
        
    #     filter_type = self.item_type.filter(categ)
    #     return filter_type

    # def save(self, *args, **kwargs):
    #     if not self.item_type:
    #         self.item_type = self.get_item_type_by_category()
    #     super().save(*args, **kwargs)

    def get_item_type_by_category(self):
        # Assuming there is a one-to-one relationship or you want the first match
        filtered_item_type = MenuItem.objects.filter(menu=self.category).first()
        return filtered_item_type


#  from product import Category
item_choice =  [  ("ORDERED", "ORDERED"),
        ("WAITING", "WAITING")]

table_choose = [('SELECT_TABLE_NO','SELECT_TABLE_NO'),("TABLE: 1","TABLE: 1"),('TABLE: 2','TABLE: 2'),('TABLE: 3','TABLE: 3'),('TABLE: 4','TABLE: 4'),('TABLE: 5','TABLE: 5'),('TABLE: 6','TABLE: 6'),('TABLE: 7','TABLE: 7'),('TABLE: 8','TABLE: 8'),('TABLE: 9','TABLE: 9'),('TABLE: 10','TABLE: 10')]

class Order_Item(models.Model): 
    img = models.ImageField(upload_to = img_upload_path,blank = True,null = True)
    table_no = models.TextField(choices=table_choose,default="SELECT_TABLE_NO")
    category = models.ForeignKey(Menu, on_delete = models.CASCADE)
    item_type = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    product_items = models.ForeignKey(ProductItem, on_delete = models.CASCADE)
    # items_image = 
    quantity = models.PositiveIntegerField(blank=True,null=True)
    total_price = models.PositiveIntegerField(blank=True,null=True)
    get_order  = models.TextField(choices = item_choice,default = "WAITING")
    generated_by = models.CharField(max_length = 255)

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        if self.product_items.price is None or self.quantity is None:
            return 0
        return self.quantity * self.product_items.price

    def __str__(self):
        return self.product_items.item_name
  

    def clean(self):
        if self.table_no == "SELECT_TABLE_NO":
            raise ValidationError("please table no to continue")
         
    @staticmethod
    def filter_product_items_by_category(category_id, item_type_id):
        return ProductItem.filter_by_category_and_item_type(category_id, item_type_id)
    


class StockManagement(models.Model):
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
    product_item = models.ForeignKey(ProductItem,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    price = models.PositiveIntegerField(blank=True,null=True)
    quantity = models.PositiveIntegerField(blank = True,null = True)
    # product_deduce = models.PositiveIntegerField(blank=True,null = True)
    # now_available = models.PositiveIntegerField(blank = True,null = True)
    total_price = models.PositiveIntegerField(blank=True,null=True)

    
    # def save(self,*args,**kwargs):
    #     self.now_available = self.calc_now_available()
    #     self.total_price = self.calc_total_price()
    #     self.clean() 
    #     super().save(*args,**kwargs)


    # def calc_now_available(self):
    #     # if self.quantity is None or  self.product_deduce is None:
    #     #     return 0
    #     quantity = self.quantity if self.quantity is not None else 0

    #     product_deduce = self.product_deduce if self.product_deduce is not None else 0
    #     cal = quantity - product_deduce
    #     return max(cal, 0)

    # def __str__(self):
    #     return self.product_item.price

    
    def save(self,*args,**kwargs):
        # self.price = self.product_item.price
        self.total_price = self.calc_total_price()
        super().save(*args,**kwargs)
    
    def calc_total_price(self):
        if self.product_item.price is None or self.quantity is None:
            return 0
        return self.product_item.price * self.quantity


class Bill(models.Model):
    table_no = models.TextField()
    order_item = models.ForeignKey(Order_Item, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    paid_amount = models.PositiveIntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.table_no = self.order_item.table_no
        self.total_amount = self.order_item.total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for Order Item: {self.order_item.product_items.item_name} (Table No: {self.table_no})"

    def mark_as_paid(self):
        self.paid_amount = self.total_amount
        self.payment_status = 'Paid'
        self.save()
    # def __str__(self):
    #     return f"Bill for Table {self.table_no} - Total: {self.total_amount} NRS"
    


# class Bill(models.Model):
#     order_item = models.ForeignKey(Order_Item, on_delete=models.CASCADE)
#     table_no = models.TextField()
#     total_amount = models.PositiveIntegerField()
#     paid_amount = models.PositiveIntegerField(blank=True, null=True)
#     payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Bill for Order Item: {self.order_item.product_items.item_name} (Table No: {self.table_no})"

#     def save(self, *args, **kwargs):
#         self.table_no = self.order_item.table_no
#         self.total_amount = self.order_item.total_price
#         super().save(*args, **kwargs)

#     def mark_as_paid(self):
#         self.paid_amount = self.total_amount
#         self.payment_status = 'Paid'
#         self.save()