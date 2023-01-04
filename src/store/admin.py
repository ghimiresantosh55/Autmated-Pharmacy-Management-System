from django.contrib import admin
from .models import Location
from mptt.admin import MPTTModelAdmin
# Register your models here.

admin.site.register(Location, MPTTModelAdmin)

