from django.contrib import admin

# Register your models here.
from .models import RawData_AMPS, RawData_Weather

class RawDataWeatherAdmin(admin.ModelAdmin):
	fields = ['winddir', 'windspeedmph', 'windspdmph_avg2m', 'rainin', 'dailyrainin', 'humidity', 'tempf', 'pressure', 'timestamp', ]
	list_display = ('winddir', 'windspeedmph', 'windspdmph_avg2m', 'rainin', 'dailyrainin', 'humidity', 'tempf', 'pressure', 'timestamp')
	list_filter = ['timestamp']
	
class RawDataAMPSAdmin(admin.ModelAdmin):
	fields = ['grid', 'load', 'batt_curr', 'batt_volt', 'SP_curr', 'SP_volt', 'SP_pow', 'measured', 'predicted', 'timestamp', 'owner']
	list_display = ('grid', 'load', 'batt_curr', 'batt_volt', 'SP_curr', 'SP_volt', 'SP_pow','measured', 'predicted', 'timestamp', 'owner')
	list_filter = ['timestamp']

admin.site.register(RawData_AMPS, RawDataAMPSAdmin)
admin.site.register(RawData_Weather, RawDataWeatherAdmin)