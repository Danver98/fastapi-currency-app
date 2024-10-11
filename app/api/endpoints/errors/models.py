class UserRegistrationError(Exception):
    """Custom cluss for user registration errors"""
    def __init__(self, msg):
        self.message = msg


class CurrencyExchangeError(Exception):
    """Custom class for currency exchange errors"""
    def __init__(self, msg):
        self.message = msg
