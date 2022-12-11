import requests
import random
from django.conf import settings
from celery import shared_task

from .models import PaymentInfo
from .celery_retry import celery_retry_utils


@shared_task(bind=True, max_retries=10)
def check_payment_status(self, payment_id):
	"""
	Check status of pending payment is updated using a third party API service. 
	Using payment id for uniquely identify the payment details.
	"""
	payload = {"payment_id": payment_id}
	
	payment_status = celery_retry_utils(settings.CHECK_PAYMENT_STATUS_URL, requests.post, payload, self)

	# Updating payment status from response data
	PaymentInfo.objects.filter(payment_id=payment_id).update(payment_status=payment_status)
