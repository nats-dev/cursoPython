"""Módulo 1 - Práctica 1: conversor de unidades.

Lee el enunciado en PRACTICA_1.md.
"""

KM_POR_MILLA = 1.609344
KG_POR_LIBRA = 0.45359237


def celsius_a_fahrenheit(grados):
    """Convierte grados Celsius a Fahrenheit."""
    return grados * 9 / 5 + 32


def fahrenheit_a_celsius(grados):
    """Convierte grados Fahrenheit a Celsius."""
    return (grados - 32) * 5 / 9


def km_a_millas(km):
    """Convierte kilómetros a millas."""
    return km / KM_POR_MILLA


def millas_a_km(millas):
    """Convierte millas a kilómetros."""
    return millas * KM_POR_MILLA


def kg_a_libras(kg):
    """Convierte kilogramos a libras."""
    return kg / KG_POR_LIBRA


def libras_a_kg(libras):
    """Convierte libras a kilogramos."""
    return libras * KG_POR_LIBRA


def formatear(valor, unidad_origen, resultado, unidad_destino):
    """Devuelve el texto de la conversión con dos decimales.

    >>> formatear(100, "°C", 212.0, "°F")
    '100.00 °C = 212.00 °F'
    """
    return f"{valor:.2f} {unidad_origen} = {resultado:.2f} {unidad_destino}"


def main():
    """Muestra el menú, pide los datos e imprime el resultado."""
    print("Conversor de unidades")
    print("1. Celsius a Fahrenheit")
    print("2. Fahrenheit a Celsius")
    print("3. Kilómetros a millas")
    print("4. Millas a kilómetros")
    print("5. Kilogramos a libras")
    print("6. Libras a kilogramos")

    opcion = input("Elige una opción (1-6): ").strip()
    valor = float(input("Introduce el valor a convertir: "))

    if opcion == "1":
        resultado = celsius_a_fahrenheit(valor)
        print(formatear(valor, "°C", resultado, "°F"))
    elif opcion == "2":
        resultado = fahrenheit_a_celsius(valor)
        print(formatear(valor, "°F", resultado, "°C"))
    elif opcion == "3":
        resultado = km_a_millas(valor)
        print(formatear(valor, "km", resultado, "mi"))
    elif opcion == "4":
        resultado = millas_a_km(valor)
        print(formatear(valor, "mi", resultado, "km"))
    elif opcion == "5":
        resultado = kg_a_libras(valor)
        print(formatear(valor, "kg", resultado, "lb"))
    elif opcion == "6":
        resultado = libras_a_kg(valor)
        print(formatear(valor, "lb", resultado, "kg"))
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()