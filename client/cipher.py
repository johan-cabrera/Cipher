import json
import random

# Funciones para obtener la tabla de llaves
def fs(x, y):
    """
    Mezcla un valor primo y una semilla para generar una clave embrión.
    """
    return (x * y + 1) % 256

def fg(x, y):
    """
    Genera una clave final a partir de la clave embrión y un valor primo.
    """
    return (x + y) % 256

def fm(x, y):
    """
    Muta la semilla actual para la siguiente secuencia de cálculo de claves.
    """
    return (x ^ y) % 256

def generate_key_table(p, q, s, size=16):
    """
    Genera una tabla de claves de 8 bits a partir de P, Q y S.
    """
    key_table = []
    for _ in range(size // 2):
        p0 = fs(p, s)
        k1 = fg(p0, q)
        s0 = fm(s, q)
        key_table.append(k1)
        
        q0 = fs(q, s0)
        k2 = fg(q0, p0)
        s1 = fm(s0, p0)
        key_table.append(k2)
        
        s = s1
        
    return key_table

# Funciones de Cifrado Polimórfico 
def xor_cipher(data, key):
    """Aplica una operación XOR."""
    return data ^ key

def add_cipher(data, key):
    """Aplica una suma modular."""
    return (data + key) % 256

def sub_cipher(data, key):
    """Aplica una resta modular."""
    return (data - key) % 256

def encrypt_message(message: str, key_table: list[int]) -> str:
    """
    Cifra un mensaje usando una tabla de claves y el PSN.

    Args:
        message(str): Mensaje original que se quiere cifrar.
        ket_table(list[int]): tabla de llaves para encriptar 
    """
    # Generamos un PSN aleatorio para iniciar la secuencia de cifrado.
    initial_psn = random.randint(0, 15)
    
    # El mensaje se convierte a bytes para su cifrado.
    message_bytes = message.encode('utf-8')
    
    # Lista para almacenar los bytes encriptados.
    encrypted_bytes = []
    
    # Se usa una copia del PSN para el bucle y la actualización.
    psn = initial_psn
    
    for i, b in enumerate(message_bytes):
        key = key_table[i % len(key_table)]
        
        # El modo de operación depende del psn actual.
        mode = psn % 3
        
        if mode == 0:
            c = xor_cipher(b, key)
        elif mode == 1:
            c = add_cipher(b, key)
        else: # mode == 2
            c = sub_cipher(b, key)
        
        encrypted_bytes.append(c)
        
        # El psn se actualiza con el valor del byte original.
        psn = (psn + b) % 16
    
    # Añadimos el PSN inicial al inicio del mensaje encriptado.
    final_bytes = bytes([initial_psn]) + bytes(encrypted_bytes)
    return final_bytes.hex()

def decrypt_message(encrypted_message: str, key_table: list[int]) -> str:
    """
    Descifra un mensaje encriptado, extrayendo el PSN inicial.
    """
    # El mensaje se convierte de cadena hexadecimal a bytes.
    encrypted_bytes = bytes.fromhex(encrypted_message)
    
    # El primer byte es el PSN inicial, lo extraemos.
    psn = encrypted_bytes[0]
    ciphertext_bytes = encrypted_bytes[1:]
    
    # Lista para los bytes desencriptados.
    decrypted_bytes = []
    
    for i, c in enumerate(ciphertext_bytes):
        key = key_table[i % len(key_table)]
        
        # El modo de operación se determina con el psn actual.
        mode = psn % 3

        if mode == 0:
            b = xor_cipher(c, key)
        elif mode == 1:
            b = sub_cipher(c, key)
        else: # mode == 2
            b = add_cipher(c, key)

        decrypted_bytes.append(b)
        
        # El psn se actualiza con el valor del byte descifrado.
        psn = (psn + b) % 16
            
    return bytes(decrypted_bytes).decode('utf-8')

# --- Funciones de I/O ---
def save_message(sender, encrypted_message):
    """
    Guarda un mensaje encriptado en el archivo messages.json.
    """
    message_data = {
        "sender": sender,
        "message": encrypted_message
    }
    
    try:
        with open("../data/messages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []
    
    messages.append(message_data)
    
    with open("../data/messages.json", "w") as file:
        json.dump(messages, file, indent=4)

def load_messages():
    """
    Carga los mensajes encriptados del archivo messages.json.
    """
    try:
        with open("../data/messages.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []