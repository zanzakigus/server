import random
import string


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_number(length: int):
    cadena = ""
    for _ in range(length):
        cadena += str(random.randint(0, 9))
    return cadena
