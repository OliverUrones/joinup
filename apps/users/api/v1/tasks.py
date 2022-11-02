from djangoapp.settings import env
from apps.users.api.v1.utils import EmailSender, SmsSender
from djangoapp.celeryapp import app
from celery import group
from requests.exceptions import RequestException


def async_tasks(user):
    """
    Function to create asynchronous tasks with user data needed to send email en sms
    """
    # Create tasks
    task_send_email = send_email.s(user.email, '{0} {1}'.format(user.first_name, user.last_name), 'https://domain.com/api/v1/validation_email/')
    task_send_sms = send_sms.s(user.phone.as_e164, 'Valide su teléfono')

    # Set queue
    task_send_email = task_send_email.set(queue='email')
    task_send_sms = task_send_sms.set(queue='sms')

    # Group task to execute in parallel
    tasks_group = group(task_send_email, task_send_sms)

    return tasks_group.apply_async()


@app.task(autoretry_for=(RequestException,), retry_backoff=True, max_retries=5)
def send_email(to_email, full_name, validation_link):
    """
    Function to send email. Config to autoretry 5 time max. when a Request exception is happened with a retry backoff algorithm.
    """
    # email_sender = EmailSender(to_email=to_email, user_name=full_name, validation_url=validation_link)
    # resp = email_sender.send_email()
    resp = True

    if resp:
        return 0
    else:
        return -1


@app.task(autoretry_for=(RequestException,), retry_backoff=True, max_retries=5)
def send_sms(to_phone, text):
    """
    Function to send sms. Config to autoretry 5 time max. when a Request exception is happened with a retry backoff algorithm.
    """
    # sms_sender = SmsSender(to_phone=to_phone, text=text)
    # message = sms_sender.send_sms()
    message = True

    if message:
        return 0
    else:
        return -1