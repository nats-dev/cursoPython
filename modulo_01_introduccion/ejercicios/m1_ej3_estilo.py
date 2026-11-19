"""Módulo 1 - Ejercicio 3: código con estilo.

La función de abajo funciona, pero ignora PEP 8. Reescríbela siguiendo las
indicaciones del enunciado sin cambiar su comportamiento.
"""

IVA_GENERAL = 21


def precio_final(precio, iva=21, descuento=0):
    """Calcula el precio final aplicando primero el descuento y luego el IVA."""
    precio_con_descuento = precio - precio * descuento / 100
    precio_con_iva = precio_con_descuento + precio_con_descuento * iva / 100
    return round(precio_con_iva, 2)