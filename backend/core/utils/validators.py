import re


REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@_$!%*#?&])[A-Za-z\d@_$!%*#?&]{8,}$"

def validate_password_complexity(password: str) -> str:
    if not re.fullmatch(REGEX_PASSWORD, password):
        raise ValueError('Password must be at least 8 characters long, 1 uppercase letter, 1 special character and 1 number')
    return password