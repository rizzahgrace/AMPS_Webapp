from django.contrib import admin

# Register your models here.
from .models import RawData_AMPS, RawData_Weather

admin.site.register(RawData_AMPS)
admin.site.register(RawData_Weather)