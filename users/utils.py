import random
from django.core.cache import cache


def generate_otp(phone):
    otp = random.randint(100000, 999999)
    cache.set(phone, otp, timeout=60)  # 1 minute
    return otp


def verify_otp(phone, otp):
    otp = int(otp)
    if cache.get(phone) == otp:
        cache.delete(phone)
        return True
    return False
