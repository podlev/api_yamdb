from django.contrib.auth.tokens import default_token_generator


def get_confirmation_code(user):
    token = default_token_generator.make_token(user)
    return token


def check_confirmation_code(user, token):
    return default_token_generator.check_token(user, token)
