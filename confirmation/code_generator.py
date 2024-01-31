import random


def generate_code() -> str:
    """
    Genera un código aleatorio de 9 caracteres con el formato XXXX-XXXX-Y, donde X es un número aleatorio entre 0 y 9
    e Y es una letra aleatoria entre A y Z, excluyendo la O y la I para evitar confusiones.
    :return: Código generado que se envia por correo al usuario
    """
    code = str(random.randint(100000, 999999))
    number = 0
    for digit in str(code):
        number += int(digit)
    letter = chr(number % 26 + 65)
    if letter == "O" or letter == "I":
        letter = chr((number + 1) % 26 + 65)
    return code[3:] + "-" + code[:3] + "-" + letter
