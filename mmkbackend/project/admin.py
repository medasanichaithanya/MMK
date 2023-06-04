from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class AccountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
   
admin.site.register(Account,AccountAdmin)
class Phone_numberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
admin.site.register(Phone_number,Phone_numberAdmin)