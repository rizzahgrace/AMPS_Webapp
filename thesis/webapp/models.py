from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User

class RawData_Weather(models.Model):
	winddir = models.IntegerField(null=True)
	windspeedmph = models.FloatField(null=True)
	windspdmph_avg2m = models.FloatField(null=True)
	rainin = models.FloatField(null=True)
	dailyrainin = models.FloatField(null=True)
	humidity = models.FloatField(null=True)
	tempf = models.FloatField(null=True)
	pressure = models.FloatField(null=True)
	timestamp = models.DateTimeField('date logged', default = now)

class RawData_AMPS(models.Model):
	grid = models.FloatField(null=True)
	load = models.FloatField(null=True)
	batt_curr = models.FloatField(null=True)
	batt_volt = models.FloatField(null=True)
	batt_pow = models.FloatField(null=True)
	SP_curr = models.FloatField(null=True)
	SP_volt = models.FloatField(null=True)
	SP_pow = models.FloatField(null=True)
	# measured = models.FloatField(null=True)
	# predicted = models.FloatField(null=True)
	timestamp = models.DateTimeField('date logged', default = now)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)