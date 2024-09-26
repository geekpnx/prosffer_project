from django.contrib import admin
from django.contrib.auth.models import User

from . import models


class ConsumerAdmin(admin.ModelAdmin):
     list_display =  ['user', 'phone_number', 'date_of_birth', 'address'] 


admin.site.register(models.Consumer, ConsumerAdmin) 



#ConsumerAdmin)# Register your models here.

# class UserInLine(admin.StackedInline):
#     model = User
#     readonly_fields = ("username", "password",)
#     extra = 1


# class ConsumerAdmin(admin.ModelAdmin):
#     inlines =  (UserInLine, ) 