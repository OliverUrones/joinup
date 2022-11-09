from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from phonenumber_field.serializerfields import PhoneNumberField

from djangoapp.settings import env, ENVIRONMENT
from apps.users.models import Profile
from apps.users.api.v1.utils import EmailSender, SmsSender

from apps.users.api.v1.tasks import async_tasks


class ProfileSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Profile.objects.all())])
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(write_only=True, allow_blank=False)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'hobbies', 'password',)
        write_only = ('password')

    def create(self, validated_data):
        user = Profile.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            hobbies=validated_data['hobbies']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        if ENVIRONMENT.lower() == 'prod':
            # SENDERS SYNCHRONOUS
            # Send Email
            # email_sender = EmailSender(to_email=user.email, user_name='{0} {1}'.format(user.first_name, user.last_name), validation_url='https://domain.com/api/v1/validation_email/')
            # email_sender.send_email()

            # Send sms
            # sms_sender = SmsSender(to_phone=user.phone, text='Valide su teléfono')
            # sms_sender.send_sms()

            # SENDERS ASYNCHRONOUS
            async_tasks(user)

        return user


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'hobbies', 'validated_email', 'validated_phone')
