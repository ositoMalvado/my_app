def github_to_raw(url):
    # Dividir la URL en partes
    parts = url.split('/')

    # Verificar si es una URL de GitHub
    if 'github.com' not in parts:
        return "La URL proporcionada no es de GitHub"

    # Encontrar el índice de 'github.com' en la URL
    github_index = parts.index('github.com')

    # Construir la nueva URL
    raw_url = 'https://raw.githubusercontent.com'
    
    # Agregar el resto de la ruta, saltando 'github.com' y eliminando 'blob' si está presente
    for part in parts[github_index + 1:]:
        if part != 'blob':
            raw_url += '/' + part

    return raw_url