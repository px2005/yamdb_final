from rest_framework_simplejwt.tokens import AccessToken


def get_token_for_user(user):
    token = AccessToken.for_user(user)
    return {
        'token': str(token),
    }


class SerializerKwargValue:
    requires_context = True

    def __init__(self, kwarg_id):
        self.kwarg_id = kwarg_id

    def __call__(self, serializer_field):
        return serializer_field.context['request'].parser_context['kwargs'][
            self.kwarg_id
        ]
