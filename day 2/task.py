import re
from datetime import datetime


def parse_text(value):
    if value is None or value.strip() == "":
        return None
    return value.strip()

def parse_int(value):
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None

def parse_date(value):
    if not value or not isinstance(value, str):
        return None
    value = value.strip()
    if not re.fullmatch(r"\d{1,2}.\d{1,2}.\d{4}$", value):
        return None
    try:
        day, month, year = map(int, value.split("."))
        return datetime(year, month, day)
    except ValueError:
        return None

def required(value):
    return value is not None and len(str(value)) > 0

def not_empty(value):
    return isinstance(value, str) and len(value.strip()) > 0

def min_length(min_len):
    def validator(value):
        if value is None:
            return False
        return len(value) >= min_len
    return validator

def max_length(max_len):
    def validator(value):
        if value is None:
            return False
        return len(value) <= max_len
    return validator

def min_value(min_val):
    def validator(value):
        if value is None:
            return False
        return value >= min_val
    return validator

def max_value(max_val):
    def validator(value):
        if value is None:
            return False
        return value <= max_val
    return validator

def after_date(date_limit):
    def validator(value):
        if value is None:
            return False
        return value >= date_limit
    return validator

def before_date(date_limit):
    def validator(value):
        if value is None:
            return False
        return value <= date_limit
    return validator

def in_past(value):
    if value is None:
        return False
    today = datetime.now().date()
    return value.date() < today

def in_future(value):
    if value is None:
        return False
    today = datetime.now().date()
    return value.date() > today

def phone(value):
    if not isinstance(value, str):
        return False
    return re.fullmatch(r"\+7\d{10}", value.strip()) is not None

def email(value):
    if not isinstance(value, str):
        return False
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value.strip()) is not None

def compose(*validators):
    def composed_validator(value):
        for validator in validators:
            if not validator(value):
                return False
        return True
    return composed_validator

def single_validator(parse_func, validate_func):
    def validator(raw_value):
        parsed = parse_func(raw_value)
        return validate_func(parsed)
    return validator

def multi_validator(fields):
    def validator(form_data):
        results = {}
        for field_name, field_validator in fields.items():
            raw_value = form_data.get(field_name)
            results[field_name] = field_validator(raw_value)
        return results
    return validator


if __name__ == "__main__":
    phone_validator = single_validator(
        parse_text,
        compose(required, phone)
    )
    score_validator = single_validator(
        parse_int,
        compose(required, min_value(60), max_value(200))
    )

    date_validator = single_validator(
        parse_date,
        in_past
    )

    mail_validator = single_validator(
        parse_text,
        compose(required, email)
    )

    print(phone_validator("+78005553535"))
    print(phone_validator("abrada"))
    print(score_validator("75"))
    print(score_validator("-10"))
    print(score_validator(".80"))
    print(date_validator("19.05.2001"))
    print(date_validator("30.11.2025"))
    print(mail_validator("user-+2334@mail.com"))
    print(mail_validator("user!@example.com"))

    form_fields = {
        "name": single_validator(
            parse_text,
            compose(not_empty, max_length(100))
        ),
        "password": single_validator(
            parse_text,
            compose(required, min_length(8), max_length(40))
        ),
        "phone": single_validator(
            parse_text,
            compose(required, phone)
        ),
        "email": single_validator(
            parse_text,
            compose(required, email)
        )
    }

    form_validator = multi_validator(form_fields)

    input_data = {
        "name": "Иванов Иван Иванович",
        "password": "qwerty12",
        "phone": "+78005553535",
        "email": "user@example.com"
    }

    print(form_validator(input_data))
