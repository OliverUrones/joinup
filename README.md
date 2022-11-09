# joinup
Joinup technical test

API to create users and send email and sms synchronous and asynchronous to validation data and get profile

# INSTALLATION
## Requirements
* Python >= 3.6.9
* Erlang >= 25.0.4
* RabbitMQ >= 3.11.2
* Packages on requirements.txt file installed on virtual environment.
* Need .env file to save environment variable

# .env FILE
#### This is the file that contains the necessary environment varibles
ENVIRONMENT='prod'  
SENDGRID_FROM_ADDRESS='no-replay@joinup.es'  
SENGRID_API_KEY='YOUR_SENDGRID_API_KEY'  
SENDGRID_VALIDATION_EMAIL_TEMPLATE_ID='YOUR_TEMPLATE_ID'  
SMS_SENDER_NUMBER='000000000'  
TWILIO_ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  
TWILIO_AUTH_TOKEN='YOUR_AUTH_TOKEN'  


# ENDPOINTS
### POST api/v1/signup/
Endpoint to register users.

### POST api/v1/api-auth
Endpoint to get user token by email and password

### GET api/v1/profile/
Endpoint to get profile use data

# Asynchronous configurations
### Start Celery Worker
celery -A djangoapp.celeryapp worker -Q email,sms -E --loglevel=INFO
### Check events on worker
celery -A djangoapp.celeryapp events

### Start Rabbitmq Server
sudo rabbitmq-server
### Check queues on broker
sudo rabbitmqctl list_queues

### Start Redis Server
redis-server
