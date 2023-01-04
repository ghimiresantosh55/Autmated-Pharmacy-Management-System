'''
Function for generate random password 
'''
import random

def random_password_generator(lower_case: bool=True, upper_case: bool=False, numbers: bool = False, special_chars: bool=False, length: int=8):

    """
    random password Generator, give "True" or "False" in parameters to include or exclude letters
    Default: Lower_case = True, Upper, number, special_chars = False, length = 8
    """
   
    characters = list('abcdefghijklmnopqrstuvwxyz')

    if upper_case:
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    if numbers:
        characters.extend(list('0123456789'))

    if special_chars:
        characters.extend(list('!@#$%^&*()?><:;'))

    the_password = ''
    for x in range(length):
        the_password += random.choice(characters)

    return the_password