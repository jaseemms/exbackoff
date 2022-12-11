import requests
import random


def celery_retry_utils(url, request_method, payload, celery_instance):
	try:
		if payload:
			response = request_method(url, json=payload)
		else:
			response = request_method(url)

		# Considering status code 429 and greater than equal to 500 is irregular response.
		if response.status_code == 429 or response.status_code >= 500:
			response.raise_for_status() # Raise HTTPError

	except (requests.exceptions.Timeout, 
			requests.exceptions.ConnectionError,
			requests.exceptions.HTTPError) as e:

		# Countdown will be less than 64 seconds.
		# Randomly increase up to 59 seconds then chose value between 59 and 64 secods
		countdown = min(random.uniform(2, 3) ** celery_instance.request.retries , 2 ** random.uniform(5.9, 6))
		
		# Retrying the task and applaying jitter in exponential backoff.
		# Raise exception if maximum retry exceeds.
		raise celery_instance.retry(exc=e, countdown=round(countdown, 3))
	
	response.raise_for_status() # raise Exception if request failed
	response_data = response.json()
	payment_status = response_data["payment_status"]

	return payment_status