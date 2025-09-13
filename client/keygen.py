import random
import math

def get_prime_number(bits=8):
    """
    Función para obtener un número primo aleatorio de 'bits' bits.
    Por defecto, genera un primo de 8 bits.

    Args:
        bits (int): El número de bits que tendrá el número primo.

    Returns:
        int: Un número primo aleatorio del tamaño especificado en 'bits'.
    """
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def is_prime(n):
    """
    Función para verificar si un número es primo usando el método de prueba por división.

    Args:
        n (int): El número a verificar.

    Returns:
        bool: True si el número es primo, False en caso contrario.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i += 2
    
    return True

def get_keys(p, q):
    """
    Función que genera las claves, 'S' y sus inversas.
    'p' y 'q' son los dos números primos que generaron las claves.

    Args:
        p (int): El primer número primo.
        q (int): El segundo número primo.

    Returns:
        int: Retorna el valor de 'S'.
    """
    s = random.randint(1, p * q - 1)
    return s

def generate_params():
    """
    Genera los parámetros P, Q y S para la sesión.
    Se asegura de que P y Q sean números primos de un tamaño de 8 bits para esta simulación.

    Returns:
        dict: Un diccionario con las claves 'p', 'q' y 's'.
    """
    p = get_prime_number()
    q = get_prime_number()
    s = get_keys(p, q)
    return {
        "p": p,
        "q": q,
        "s": s
    }

def clear_params():
    """
    Borra los parámetros P, Q y S al finalizar la sesión.
    En un entorno real, esto implicaría un manejo más seguro,
    pero para esta simulación, devuelve un diccionario vacío.

    Returns:
        dict: Un diccionario vacío.
    """
    return {
        "p": None,
        "q": None,
        "s": None
    }