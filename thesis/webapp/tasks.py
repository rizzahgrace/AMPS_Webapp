from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import task
from webapp.models import RawData_AMPS
import urllib

logger = get_task_logger(__name__)


@task(name="display")
def power_data(x):
	url = "http://192.168.1.112"
	f = urllib.urlopen(link)
	myfile = f.read()

@task(name="add_numbers")
def add(x,y): 
	return x+y
