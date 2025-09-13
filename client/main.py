import auth
import keygen
import cipher
import os
import time

def clear_screen():
    """
    Limpia la pantalla de la terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(username, title):
    """
    Muestra un encabezado con el usuario actual y el título de la vista.
    """
    clear_screen()
    print("=" * 40)
    print(f"Usuario: {username}".center(40))
    print(f"--- {title} ---".center(40))
    print("=" * 40)
    print()

def main_menu(current_user):
    """
    Muestra el menú principal y maneja la interacción del usuario.

    Args:
        current_user (dict): El diccionario del usuario actualmente autenticado.
    """
    while True:
        show_header(current_user['username'], "Menú Principal")
        print("1. Sincronizar")
        print("2. Enviar Mensaje")
        print("3. Ver Mensajes")
        print("4. Desincronizar")
        print("5. Cerrar Sesión")
        choice = input("Selecciona una opción: ")

        if choice == '1':
            synchronize_option(current_user)
        elif choice == '2':
            send_message_option(current_user)
        elif choice == '3':
            view_messages_option(current_user)
        elif choice == '4':
            desynchronize_option(current_user)
        elif choice == '5':
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            time.sleep(2)  # Pausa para que el usuario pueda ver el error

def synchronize_option(user):
    """
    Lógica de sincronización para el menú.
    """
    show_header(user['username'], "Sincronizar")
    sync_id = input("Ingresa el ID de sincronización: ")
    sync_key = input("Ingresa la clave de sincronización: ")
    
    # El usuario reescribe sus propios valores de id y key.
    user['id'] = sync_id
    user['key'] = sync_key
    
    # Guarda los cambios para que el otro usuario pueda "verlos"
    users_data = auth.load_data()
    for i, u in enumerate(users_data):
        if u['username'] == user['username']:
            users_data[i] = user
            break
    auth.save_data(users_data)
    
    # Busca si hay otro usuario con el mismo id y key
    sync_user = auth.find_sync_user(sync_id, sync_key, user['username'])
    
    if sync_user and sync_user['p'] and sync_user['q'] and sync_user['s']:
        # Si se encuentra un usuario con parámetros, los copia
        user['p'] = sync_user['p']
        user['q'] = sync_user['q']
        user['s'] = sync_user['s']
        print("\033[92m\n¡Sincronización exitosa!\033[0m")
    else:
        # Si no se encuentra un usuario con parámetros, los crea
        params = keygen.generate_params()
        user['p'] = params['p']
        user['q'] = params['q']
        user['s'] = params['s']
        print("\nNo se encontró un usuario con parámetros. \nGenerando nuevos parámetros para la sesión...")

    # Guarda los parámetros P, Q y S en el archivo
    users_data = auth.load_data()
    for i, u in enumerate(users_data):
        if u['username'] == user['username']:
            users_data[i] = user
            break
    auth.save_data(users_data)
    input("\nPresiona Enter para continuar...")

def send_message_option(user):
    """
    Maneja la lógica de envío de mensajes en el menú.
    """
    show_header(user['username'], "Enviar Mensaje")
    if not user['p']:
        print("\033[91m\n¡Error! No estás sincronizado. Por favor, sincroniza primero.\033[0m")
        input("\nPresiona Enter para continuar...")
        return
    
    message_to_send = input("Escribe tu mensaje: ")
    
    key_table = cipher.generate_key_table(user['p'], user['q'], user['s'])
    encrypted_msg = cipher.encrypt_message(message_to_send, key_table)
    
    cipher.save_message(user['username'], encrypted_msg)
    print("\033[92m\nMensaje encriptado y enviado.\033[0m")
    input("\nPresiona Enter para continuar...")

def view_messages_option(user):
    """
    Maneja la lógica para ver y desencriptar mensajes.
    """
    show_header(user['username'], "Ver Mensajes")
    if not user['p']:
        print("\033[91m\n¡Error! No estás sincronizado. Por favor, sincroniza primero.\033[0m")
        input("\nPresiona Enter para continuar...")
        return
        
    messages = cipher.load_messages()
    
    if not messages:
        print("No hay mensajes para mostrar.")
    else:
        key_table = cipher.generate_key_table(user['p'], user['q'], user['s'])
        
        for msg in messages:
            try:
                decrypted_msg = cipher.decrypt_message(msg['message'], key_table)
                print(f"De: \033[92m{msg['sender']}\033[0m")
                print(f"Mensaje: {decrypted_msg}\n")
            except Exception:
                print("\033[91m\n¡Error! No se pudo desencriptar el mensaje.\033[0m")

    input("\nPresiona Enter para continuar...")


def desynchronize_option(user):
    """
    Maneja la opción de desincronización.
    """
    show_header(user['username'], "Desincronizar")
    auth.desynchronize(user)
    print("Desincronizando...")
    print("\nSe han borrado los parámetros.")
    input("\nPresiona Enter para continuar...")

def login_menu():
    """
    Muestra el menú de inicio de sesión inicial.
    """
    while True:
        clear_screen()
        print("=" * 40)
        print("Sistema de Cifrado Polimorfico OTP".center(40))
        print("--- Iniciar Sesión ---".center(40))
        print("=" * 40)
        username = input("Ingresa tu nombre de usuario: ")
        password = input("Ingresa tu contraseña: ")
        
        user = auth.login(username, password)
        if user:
            main_menu(user)
        else:
            print("\033[91m\nUsuario o contraseña incorrectos.\033[0m")
            time.sleep(2)
    
if __name__ == "__main__":
    login_menu()