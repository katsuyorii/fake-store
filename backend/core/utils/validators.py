import re
import phonenumbers


REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@_$!%*#?&])[A-Za-z\d@_$!%*#?&]{8,}$"

def validate_password_complexity(password: str) -> str:
    if not re.fullmatch(REGEX_PASSWORD, password):
        raise ValueError('Password must be at least 8 characters long, 1 uppercase letter, 1 special character and 1 number')
    return password

def validate_phone_number_format(phone_number: str) -> str:
        try:
            parsed_phone_number = phonenumbers.parse(phone_number, 'RU')
            if not phonenumbers.is_valid_number(parsed_phone_number):
                raise ValueError('Invalid phone number')
            return phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError('Incorrect format phone number')