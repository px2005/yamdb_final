import os
import struct

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from api.serializers import UserSerializer
from api_yamdb.settings import EMAIL_SENDER, EMAIL_SUBJECT
from users.models import UserProfile


class CreateUserSerializer(UserSerializer):
    class Meta:
        fields = (
            'username',
            'email',
        )
        model = UserProfile

    def create(self, validated_data):
        confirmation_code = struct.unpack('H', os.urandom(2))[0]
        send_mail(
            EMAIL_SUBJECT,
            str(confirmation_code),
            EMAIL_SENDER,
            [validated_data.get('email')],
            fail_silently=False,
        )
        validated_data['confirmation_code'] = confirmation_code
        return UserProfile.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('me')
        return value


class GetTokenSerializer(TokenObtainSlidingSerializer):
    password = serializers.HiddenField(default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.HiddenField(default='')
        self.fields['confirmation_code'] = serializers.IntegerField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confirmation_code': attrs['confirmation_code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        conf_code = get_object_or_404(
            UserProfile,
            username=attrs['username']
        ).confirmation_code

        if conf_code != attrs['confirmation_code']:
            raise serializers.ValidationError(
                {'confirmation_code': 'confirmation_code некорректный.'})
        return {}
