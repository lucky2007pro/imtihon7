import re

def check_email_or_phone(user_input):
    user_input = user_input.strip()
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    
    if email_regex.match(user_input):
        return 'email', user_input.lower()
    
    # Simple cleanup for phone numbers
    phone = re.sub(r'[^0-9+]', '', user_input)
    return 'phone', phone
