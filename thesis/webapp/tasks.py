from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import task
from webapp.models import RawData_AMPS

logger = get_task_logger(__name__)


@task(name="display")
def power_data(x):
	latestdata=RawData_AMPS.objects.get(id = x).id
	latestdata+=1
	return latestdata

@task(name="add_numbers")
def add(x,y): 
	return x+y
