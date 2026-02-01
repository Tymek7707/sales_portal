import re 

from django.core.exceptions import ValidationError


def validate_phone_number(number):
    if not re.match(r'^\d{9}$', number.strip()):
        raise ValidationError("Phone number must contain only digits (9 digits)")
    
def validate_nip(nip):
    nip = nip.strip()
    if not re.match(r'^\d{10}$', nip):
        raise ValidationError("Nip must contain only digits (exactly 10 digits)")
    
    weights = [6,5,7,2,3,4,5,6,7]

    checksum = 0
    for num in range(9):
        checksum += int(nip[num]) * weights[num]

    if checksum != int(nip[9]):
        raise ValidationError("Invalid Nip (checksum failed)")    

def validate_only_letters(word):
    if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+$', word.strip()):
        raise ValidationError("This field must contain only letters, spaces and hyphens")
    