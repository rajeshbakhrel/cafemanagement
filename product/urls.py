from django.urls import path
from . import views




urlpatterns = [
path("menulist/",views.Menu_List.as_view(),name= "category_view"),
path("menudetail/<int:pk>/",views.Menu_Detail.as_view(),name= "category_view"),
path("menuitemlist/",views.Menu_ItemList.as_view(),name= "items_view"),
path("menuitemdetail/<int:pk>/",views.Menu_ItemDetail.as_view(),name= "itemdetail_view"),

path("productlist/",views.Product_ItemList.as_view(),name = "view product_item list"),
path("productdetail/<int:pk>/",views.Product_ItemDetail.as_view(),name = "view product_detail"),
path('orderitemlist/',views.Order_ItemView.as_view()),
path('orderitemdetail/<int:pk>/',views.Order_ItemDetail.as_view()),

# for the Stock management
path("stocklist/",views.Stock_List.as_view(),name= "stock_view"),
path("stockdetail/<int:pk>/",views.Stock_Detail.as_view(),name= "stockdetail_view"),


]