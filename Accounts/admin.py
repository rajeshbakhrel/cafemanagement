from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .profile import Profile

# Register your models here.





    

# class UserAdmin(BaseUserAdmin):
  
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('id','email','name', 'contact','is_admin',)
#     list_filter = ('is_admin','is_active')
#     fieldsets = (
#         ('User Credentials', {'fields': ('email', 'password','contact')}),
#         ('Personal info', {'fields': ('name')},),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name','contact' ,'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email',)
#     ordering = ('email','id',)
#     filter_horizontal = ()
          
# # registeing the user model
# admin.site.register(User,UserAdmin)



# class ProfileAdmin(admin.ModelAdmin):
#       list_display = ['id','user_email','name','contact','image']

# admin.site.register(Profile,ProfileAdmin)      





class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'name', 'is_admin',)
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        ('User Credentials', {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'name', 'image']

admin.site.register(Profile, ProfileAdmin)

