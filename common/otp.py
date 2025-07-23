from django.utils.crypto import get_random_string

def generate_otp():
    return get_random_string(6,"1234567890")
