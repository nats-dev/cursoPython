"""Módulo 1 - Ejercicio 1: saludo."""


def saludar(nombre):
    """Devuelve un saludo de bienvenida para ``nombre``.

    El nombre se limpia de espacios sobrantes y se escribe con la inicial de
    cada palabra en mayúscula. Si queda vacío, se saluda a "Anónimo".

    >>> saludar("  ada lovelace ")
    'Hola, Ada Lovelace. ¡Te damos la bienvenida al curso!'
    """
    nombre_limpio = " ".join(nombre.split())
    if not nombre_limpio:
        nombre_limpio = "Anónimo"
    else:
        nombre_limpio = nombre_limpio.title()

    return f"Hola, {nombre_limpio}. ¡Te damos la bienvenida al curso!"

    


def main():
    """Pide el nombre por teclado e imprime el saludo."""
    
    nombre = input("Introduce tu nombre: ")
    print(saludar(nombre))


if __name__ == "__main__":
    main()
