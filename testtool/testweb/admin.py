from django.contrib import admin
from .models import AddressInfo
# Register your models here.
class AddressInfoAdmin(admin.ModelAdmin):
    list_display = ['address','pid']
admin.site.register(AddressInfo,AddressInfoAdmin)