from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from phonenumber_field.serializerfields import PhoneNumberField

from djangoapp.settings import env, ENVIRONMENT
from apps.users.models import Profile
from apps.users.api.v1.utils import EmailSender, SmsSender


class ProfileSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Profile.objects.all())])
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(write_only=True, allow_blank=False)
    password2 = serializers.CharField(write_only=True, allow_blank=False)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'hobbies', 'password', 'password2',)
        write_only = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password didn't match."})

        return attrs

    def create(self, validated_data):
        print(type(validated_data['phone']))
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
            # Send Email
            email_sender = EmailSender(to_email=user.email, user_name='{0} {1}'.format(user.first_name, user.last_name), validation_url='https://domain.com/api/v1/validation_email/')
            email_sender.send_email()

            # Send sms
            sms_sender = SmsSender(to_phone=user.phone, text='Valide su teléfono')
            sms_sender.send_sms()

        return user


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'hobbies', 'validated_email', 'validated_phone')