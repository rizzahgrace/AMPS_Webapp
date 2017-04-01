from django.shortcuts import render
from webapp.forms import UploadCSVFile, recordUser
from webapp.utils import handle_upload_file
from highcharts.views import (HighChartsMultiAxesView, HighChartsStockView)
from .models import RawData_AMPS, RawData_Weather
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
	return render(request, 'webapp/home.html')

def home(request):
	return render(request, 'webapp/home2.html')

def weather(request):
	return render(request, 'webapp/weather.html')

def power(request):
	return render(request, 'webapp/power.html')

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
		data = {'id': [], 'windspeedmph': [], 'temperature':[], 'timestamp':[]}
		f = RawData_Weather.objects.all()
		for unit in f:
			data['id'].append(unit.id)
			data['timestamp'].append(unit.timestamp.strftime('%I:%M'))
			data['windspeedmph'].append(unit.windspeedmph)
			data['temperature'].append(unit.tempf)


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
			'name': 'windspeedmph',
			'data': data['windspeedmph']
			},
			{
			'name': 'temperature',
			'data': data['temperature']
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
		data = {'id': [], 'load': [], 'SP_pow':[], 'timestamp':[]}
		f = RawData_AMPS.objects.filter(owner = User.objects.get(username=self.request.user))[:10]
		for unit in f:
			data['id'].append(unit.id)
			data['timestamp'].append(unit.timestamp.strftime('%I:%M'))
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
			'name': 'Load',
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
