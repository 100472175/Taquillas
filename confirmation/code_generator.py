import random

def generate_code() -> str:
    code = str(random.randint(100000, 999999))
    number = 0
    for digit in str(code):
        number += int(digit)
    letter = chr(number % 26 + 65)
    if letter == "O" or letter == "I":
        letter = chr((number + 1) % 26 + 65)
    return code[3:] + "-" + code[:3] + "-" + letter