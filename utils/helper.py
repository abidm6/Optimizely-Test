import time as sleep_time
from datetime import datetime
import string
import random
from datetime import *
from selenium.webdriver.support import expected_conditions as ec
def wait_for_next_minute():
    # Check the current second is between 40 to 59 seconds. If it is then waiting 20 seconds.
    myobj = datetime.now()
    print(myobj.second)
    if (40 <= myobj.second and myobj.second <= 59):
        print('waiting 20 seconds')
        sleep_time.sleep(20)

def generate_password(length=15):
    # define all possible characters
    chars = string.ascii_letters + string.digits + string.punctuation
    # ensure the password includes at least one lowercase letter, one uppercase letter, one special character, and one digit
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        if (any(char.islower() for char in password)
                and any(char.isupper() for char in password)
                and any(char in string.punctuation for char in password)
                and any(char.isdigit() for char in password)):
            break

    return password

def generate_custom_id(length: int) -> str:
    """
        Generates a custom id.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_alphanumeric_string(string_lenght=10):
    """
    Generates random alphanumeric string for specified length.
    :param string_lenght: length of the expected random string. Default length is 10.
    :return: alphanumeric string of specified length.
    """
    alpha_numeric_string = string.ascii_letters + string.digits
    return ''.join(random.choice(alpha_numeric_string) for _ in range(string_lenght))

def get_time_difference(start_time, end_time):
    m2 = start_time
    m2 = datetime.strptime(m2, '%I:%M %p')
    print(m2)
    m3 = end_time
    m3 = datetime.strptime(m3, '%I:%M %p')

    print(m3 - m2)
    difference = m3 - m2
    hour_minute_array = str(difference).split(':')

    hour = hour_minute_array[0]+'h'
    minute = hour_minute_array[1]+'m'
    return hour, minute

def time_to_seconds(time_str):
    # Split the time string into hours, minutes, and seconds
    time_components = reversed(time_str.split(':')) # seconds, mins, hours if any
    
    total_time_in_seconds = sum([60 ** index * int(item) 
                                                     for index, item in enumerate(time_components)])

    return total_time_in_seconds

def seconds_to_mm_ss(seconds):
    if seconds < 0:
        raise ValueError("Duration cannot be negative")
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02}"
