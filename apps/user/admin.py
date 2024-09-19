from django.contrib import admin
# from django.contrib.auth.models import User

from . import models
# Register your models here.

# class UserInLine(admin.StackedInline):
#     model = User
#     readonly_fields = ("username", "password",)
#     extra = 1


# class ConsumerAdmin(admin.ModelAdmin):
#     inlines =  (UserInLine, ) 


admin.site.register(models.Consumer) #ConsumerAdmin)