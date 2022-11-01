from djangoapp.settings import env
from sendgrid import sendgrid
from twilio.rest import Client


class EmailSender:
    """
    Class to send emails through sendgrid client
    """
    from_email = env('SENDGRID_FROM_ADDRESS')
    sg_client = sendgrid.SendGridAPIClient(env('SENGRID_API_KEY'))

    def __init__(self, to_email, user_name, validation_url):
        """
        Construct method
        :param to_email: Address to send email
        :param user_name: User full name
        :param validation_url: Validation email url
        """
        self.payload = {
            "from": {
                "email": self.from_email
            },
            "personalizations": [
                {
                    "dynamic_template_data": {
                        "name": user_name,
                        "validation_url": validation_url
                    },
                    "subject": "Validación de email",
                    "to": [
                        {
                            "email": to_email
                        }
                    ]
                }
            ],
            "template_id": env('SENDGRID_VALIDATION_EMAIL_TEMPLATE_ID')
        }

    def send_email(self):
        """
        Method to send email
        :return: Response sengrid API client
        """
        resp = self.sg_client.mail.send.post(request_body=self.payload)
        return resp


class SmsSender:
    """
    Class to send sms through Twilio client
    """
    twilio_account_sid = env('TWILIO_ACCOUNT_SID')
    auth_token = env('TWILIO_AUTH_TOKEN')
    from_number = env('SMS_SENDER_NUMBER')
    twilio_client = Client(twilio_account_sid, auth_token)

    def __init__(self, to_phone, text):
        """
        Construct method
        :param to_phone: Phone number to send sms
        :param text: Text of sms
        """
        self.to_phone = to_phone
        self.from_phone = env('SMS_SENDER_NUMBER')
        self.body = text

    def send_sms(self):
        """
        Method to send sms
        :return: Message twilio object
        """
        message = self.twilio_client.create(
            self.to_phone,
            self.from_phone,
            self.body
        )
        return message
