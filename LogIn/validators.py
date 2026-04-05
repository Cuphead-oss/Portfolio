
from django.core.exceptions import ValidationError

def password_valid(value):
    print("value----------------------",value)
    if len(value)<7:
        raise ValidationError("Password lenght should be 8 character or more")
    return value