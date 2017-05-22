from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import task

import uuid, requests

logger = get_task_logger(__name__)


# @task(name="text_data")
# def chikka_text():
# 	url="https://post.chikka.com/smsapi/request"
# 	results=dataprocessing(Plant.objects.filter(pk=1))
# 	message_data=str(results.values())
# 	data={'message_type':'SEND','mobile_number':'639177201795','shortcode':'29290447292','message_id':generate_msgid(),'message': message_data ,'client_id':'3cb0a832ae426c46e13f2d0d0f187986168d7c89bee9a3970415b807f34f3053','secret_key':'2c7d84869fece5bc65bddeee04cca332387388af2e6aaecba7421056731ef761'}
# 	r=requests.post(url, data=data).text
# 	print(r)

# to start the worker enter 'python manage.py celery worker --loglevel=info'
@task(name="get_rpi_data")
def rpidata():
	url="https://128.199.158.44:8001/webapp/weather"
	r=requests.get(url, 
	print(r)

@task(name = "add_numbers")
def add(x,y): 
	return x+y

def generate_msgid():
	return uuid.uuid4().hex

#modify rpi code to post values to the form
# import requests

# url = 'http://url.com'
# query = {'field': value}
# res = requests.post(url, data=query)
# print(res.text)
