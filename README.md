## Description:

If payment details are successfully submitted by using the payment info endpoint, celery background task will trigger to access the external endpoint for payment status update.
If that external API call failure is because of an irregular response or failure then the celery task will be retried using exponential backoff and jitter value, retry countdown time will be less than 64 seconds and exponentially increase from 0 to 64 seconds.
The number of API retry values will be 10, after maximum retry, the celery task will raise an exception in logs.

## Installation steps

Make sure docker and docker-compose packages are installed in your system

To run the application

1. clone the git repository in your system

2. go to the project directory where the docker-compose.yaml file is created
		
		cd payment_gateway

3. open .env file to update CHECK_PAYMENT_STATUS_URL variable, and update to an API endpoint that generates an irregular response.

4. enable execution permission for file entrypoint.sh
		
		chmod +x entrypoint.sh 

5. build the docker images using docker-compose build command
		
		docker-compose build

6. run containers using docker-compose up command, by default the service will run on port 8000 using Nginx and Gnunicorn server.
		
		docker-compose up

7. open new terminal window and enable shell access to payment_gateway_web and create new django user
		
		docker ps	- to get container id
		docker exec -it <container_id> /bin/sh
		python manage.py createsuperuser
		exit

8. Use postman or curl to interact with API endpoints and observe the docker-compose output log to check external API call and celery retry.

## List of APIs to interact with service

	1. get access token using superuser and password creared via docker shell
				endpoint : localhost:8000/users/api-token-auth/
				method: POST
				request type: json
				request body: { "username": "<useranme>", "password":"password" }
				respose: { "token": "token" }
				
	2. create payment details
				endpoint: localhost:8000/payment-info/payments/
				method: POST
				request type: json
				header: Authorization Token <access_token>
				request body: { "amount": "<float value>" }
				response: {
								"payment_id": "<uuid>",
								"created_at": "<datetime>",
								"processed_at": <null or datetime>,
								"amount": "<float value>",
								"payment_status": "<status>" # pending, failed or completed
							}
	3. list all payment info of the authenticated user
		
				endpoint: localhost:8000/payment-info/payments/
				method: GET
				request type: json
				header: Authorization Token <access_token>
				response: [{
								"payment_id": "<uuid>",
								"created_at": "<datetime>",
								"processed_at": <null or datetime>,
								"amount": "<float value>",
								"payment_status": "<status>" # pending, failed or completed
							}]
	4. check payment info using payment id
				endpoint: localhost:8000/payment-info/payments/<payment_id>/
				method: GET
				request type: json
				header: Authorization Token <access_token>
				response: {
								"payment_id": "<uuid>",
								"created_at": "<datetime>",
								"processed_at": <null or datetime>,
								"amount": "<float value>",
								"payment_status": "<status>" # pending, failed or completed
							}
		
		
### Notes: 
	
check celery logs to find details of celery retry and exponential backoff
	
If the external endpoint is failed then payment processing status will be pending