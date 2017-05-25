from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.cache import cache
from django.utils import timezone
from django.contrib import messages
from webapp.forms import UploadCSVFile, recordUser, recordWeather, recordPower
from webapp.utils import handle_upload_file
from highcharts.views import (HighChartsMultiAxesView, HighChartsStockView)
from .models import RawData_AMPS, RawData_Weather
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Count, Avg, DateTimeField	
from django.db.models.functions import Trunc
# Create your views here.

def index(request):
	return render(request, 'webapp/home.html')

def home(request):
	return render(request, 'webapp/home2.html')

def weather(request):
	data = RawData_Weather.objects.last()
	return render(request, 'webapp/weather.html', {"data":data})

def power(request):
	# data = RawData_AMPS.objects.filter(owner = request.user).last()
	return render(request, 'webapp/power1.html', {"data":fetch_recent_data(request.user)})

def csv(request):
	if request.method == 'POST':
		form = UploadCSVFile(request.POST, request.FILES)	
		
		if form.is_valid():
			owner = form.cleaned_data['owner']
			handle_upload_file(request.FILES['csvfile'], owner)
			messages.success(request, 'Record saved')
	else:
		form = UploadCSVFile()

	return render(request, 'webapp/csv.html', {'form': form})

def weatherdata(request):
	if request.method == 'POST':
		form = recordWeather(request.POST)
		if form.is_valid():
			winddir = form.cleaned_data['winddir']
			windspeedmph = form.cleaned_data['windspeedmph']
			windspdmph_avg2m = form.cleaned_data['windspdmph_avg2m']
			rainin = form.cleaned_data['rainin']
			dailyrainin = form.cleaned_data['dailyrainin']
			humidity = form.cleaned_data['humidity']
			pressure = form.cleaned_data['pressure']
			dt = timezone.now()
			dt = dt.replace(second=0, microsecond=0)
			record = RawData_Weather(winddir=winddir, windspeedmph=windspeedmph, windspdmph_avg2m=windspdmph_avg2m, rainin=rainin, dailyrainin=dailyrainin, humidity=humidity, pressure=pressure, timestamp = dt)
			record.save()
			messages.success(request, 'Record saved')
	else:
		form = recordWeather()

	return render(request, 'webapp/recordweather.html', {'form': form})

def powerdata(request):
	if request.method == 'POST':
		form = recordPower(request.POST)

		if form.is_valid():
			grid = form.cleaned_data['grid']
			load = form.cleaned_data['load']
			batt_curr = form.cleaned_data['batt_curr']
			batt_pow = form.cleaned_data['batt_pow']
			SP_curr = form.cleaned_data['SP_curr']
			SP_volt = form.cleaned_data['SP_volt']
			dt = timezone.now()
			dt = dt.replace(second=0, microsecond=0)
			record = RawData_AMPS(grid=grid, load=load, batt_curr=batt_curr, batt_pow=batt_pow, SP_curr=SP_curr, SP_volt=SP_volt, timestamp = dt)
			if (RawData_Weather.check_time(record)):
				record.save()
				messages.success(request, 'Record saved')
				#return HttpResponseRedirect(reverse('hmain:hmain'))
			else:
				messages.error(request, 'Wrong time')
	else:
		form = recordPower()
	return render(request, 'webapp/recordpower.html', {'form': form})

@csrf_protect
def register(request):
	if request.method == 'POST':
		user_form = recordUser(request.POST)
		if user_form.is_valid():
			user = User.objects.create_user(
			username=user_form.cleaned_data['username'],
			password=user_form.cleaned_data['password1'],
			email=user_form.cleaned_data['email'],
			first_name=user_form.cleaned_data['first_name'],
			last_name=user_form.cleaned_data['last_name']
			)
	else:
		user_form = recordUser()
	return render(request, 'webapp/registration.html', {'user_form' : user_form})

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('webapp/home/')
    return render_to_response('webapp/login.html', RequestContext(request))

# def test_display_historical(request):
# 	# processed_data = RawData_Weathe r.objects.filter(timestamp=).aggregate(Avg('load'))
# 	return render(request, 'webapp/index.html')#, processed_data)

def fetch_recent_data(user, lifetime=60):
	data = cache.get(user)
	if data = None:
		update_data.delay(user, lifetime)
		data = None
	else:
		recent, expiry = data
		if exprixy < datetime.datetime.now()
		update_data.delay(user, lifetime)
	return data

class AdvancedGraph(HighChartsMultiAxesView):
	title = 'Weather Data'
	subtitle = ''
	chart_type = ''
	chart = {'zoomType': 'xy'}
	tooltip = {'shared': 'true'}
	legend = {
		'layout': 'vertical',
		'align': 'left',
		'verticalAlign': 'top',
		'y': 30
	}

	def get_data(self):
		data = {'id': [], 'windspeedmph': [], 'temperature':[], 'timestamp':[], 'rainin':[], 'humidity':[], 'pressure':[]}
		f = RawData_Weather.objects.all().order_by('-id')[:10][::-1]
		for unit in f:
			data['id'].append(unit.id)
			data['timestamp'].append(unit.timestamp.strftime('%I:%M %p'))
			data['windspeedmph'].append(unit.windspeedmph)
			data['temperature'].append(unit.tempf)
			data['rainin'].append(unit.rainin)
			data['humidity'].append(unit.humidity)
			data['pressure'].append(unit.pressure)


		self.categories = data['timestamp']
		 	
		self.yaxis = {
			'title': {
				'text': ''
			},
			'plotLines': [
				{
					'value': 0,
					'width': 1,
					'color': '#808080'
				}
			]
		}
		self.serie = [
			{
			'name': 'Humidty',
			'data': data['humidity']
			},
			{
			'name': 'Pressure',
			'data': data['pressure']
			},
			{
			'name': 'Rainfall',
			'data': data['rainin']
			},
			{
			'name': 'Temperature',
			'data': data['temperature']
			},
			{
			'name': 'Wind Speed',
			'data': data['windspeedmph']
			}

		]

		##### X LABELS
		# self.axis = data['id']
		

		##### SERIES WITH VALUES
		self.series = self.serie
		data = super(AdvancedGraph, self).get_data()
		return data

class PowerGraph(HighChartsMultiAxesView):
	title = 'Power'
	subtitle = ''
	chart_type = ''
	chart = {'zoomType': 'xy'}
	tooltip = {'shared': 'true'}
	legend = {
		'layout': 'vertical',
		'align': 'left',
		'verticalAlign': 'top',
		'y': 30
	}


	def get_data(self):
		data = {'id': [], 'SP_pow':[], 'timestamp':[], 'load':[]}
		f = RawData_AMPS.objects.filter(owner = User.objects.get(username=self.request.user)).order_by('-id')[:10][::-1]
		# f = RawData_AMPS.objects.filter(owner = User.objects.get(username='rizzah')).order_by('-id')[:10][::-1]
		for unit in f:
			data['id'].append(unit.id)
			data['timestamp'].append(unit.timestamp.strftime('%I:%M %p'))
			data['load'].append(unit.load)
			data['SP_pow'].append(unit.SP_pow)


		self.categories = data['timestamp']
		
		self.yaxis = {
			'title': {
				'text': 'Title 1'
			},
			'plotLines': [
				{
					'value': 0,
					'width': 1,
					'color': '#808080'
				}
			]
		}
		self.serie = [
			{
			'name': 'Load Consumption',
			'data': data['load']
			},
			{
			'name': 'Power Generated',
			'data': data['SP_pow']
			} 
		]

		##### X LABELS
		# self.axis = data['id']
		
		##### SERIES WITH VALUES
		self.series = self.serie
		data = super(PowerGraph, self).get_data()
		return data

# class HourlyPower(HighChartsMultiAxesView):
# 	title = 'Power'
# 	subtitle = ''
# 	chart_type = ''
# 	chart = {'zoomType': 'xy'}
# 	tooltip = {'shared': 'true'}
# 	legend = {
# 		'layout': 'vertical',
# 		'align': 'left',
# 		'verticalAlign': 'top',
# 		'y': 30
# 	}
# 	def get_data(self):
# 		# data = {'id': [], 'load': [], 'SP_pow':[], 'timestamp':[]}
# 		data = {'load': [], 'timestamp':[]}
# 		# f = RawData_AMPS.objects.filter(owner = User.objects.get(username=self.request.user))[:10]
# 		f = RawData_AMPS.objects.filter(owner = User.objects.get(username='julius')).annotate(start_day=Trunc('timestamp', 'day', output_field=DateTimeField())).values('start_day').aggregate(load_day=Avg('load'))
# 		for unit in f:
# 			# data['id'].append(unit.id)
# 			data['timestamp'].append(unit.start_day)
# 			data['load'].append(unit.load_day)
# 			# data['SP_pow'].append(unit.SP_pow)


# 		self.categories = data['timestamp']
		
# 		self.yaxis = {
# 			'title': {
# 				'text': 'Title 1'
# 			},
# 			'plotLines': [
# 				{
# 					'value': 0,
# 					'width': 1,
# 					'color': '#808080'
# 				}
# 			]
# 		}
# 		self.serie = [
# 			{
# 			'name': 'Load',
# 			'data': data['load']
# 			}
# 			# {
# 			# 'name': 'Power Generated',
# 			# 'data': data['SP_pow']
# 			# } 
# 		]

# 		##### X LABELS
# 		# self.axis = data['id']
		
# 		##### SERIES WITH VALUES
# 		self.series = self.serie
# 		data = super(HourlyPower, self).get_data()
# 		return data
