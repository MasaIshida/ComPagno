import random, string


def create_cookie_value():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


