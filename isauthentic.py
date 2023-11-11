import re 

def is_valid_email(string):
   binary_pattern=re.compile(r"^[a-zA-Z0-9_.+-]+@gmail.com$")
   return bool(binary_pattern.match(string))

def is_valid_phone_no(phone_number):
   pattern = r'^[1-9]\d{9}$'
   return bool(re.match(pattern, phone_number))

