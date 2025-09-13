import json

def load_data():
    """
    Carga los datos de los usuarios desde el archivo users.json.
    
    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un usuario.
    """
    try:
        with open('../data/users.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """
    Guarda los datos de los usuarios en el archivo users.json.

    Args:
        data (list): La lista de diccionarios con los datos actualizados.
    """
    with open('../data/users.json', 'w') as file:
        json.dump(data, file, indent=4)

def login(username, password):
    """
    Verifica las credenciales de un usuario y devuelve su información si son válidas.

    Args:
        username (str): El nombre de usuario a autenticar.
        password (str): La contraseña a verificar.

    Returns:
        dict: Un diccionario con la información del usuario si el inicio de sesión es exitoso,
        o None en caso contrario.
    """
    users = load_data()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def find_sync_user(session_id, session_key, current_user_username):
    """
    Busca otro usuario con el mismo ID y clave de sincronización.

    Args:
        session_id (str): El ID de la sesión a buscar.
        session_key (str): La clave de la sesión.
        current_user_username (str): El nombre del usuario actual para no encontrarlo a él mismo.

    Returns:
        dict: La información del usuario sincronizado si se encuentra, o None.
    """
    users = load_data()
    for user in users:
        if user['id'] == session_id and user['key'] == session_key and user['username'] != current_user_username:
            return user
    return None

def desynchronize(user):
    """
    Limpia los parámetros de sincronización y las claves de un usuario.

    Args:
        user (dict): El diccionario del usuario a desincronizar.
    """
    user['id'] = None
    user['key'] = None
    user['p'] = None
    user['q'] = None
    user['s'] = None
    users_data = load_data()
    for i, u in enumerate(users_data):
        if u['username'] == user['username']:
            users_data[i] = user
            break
    save_data(users_data)