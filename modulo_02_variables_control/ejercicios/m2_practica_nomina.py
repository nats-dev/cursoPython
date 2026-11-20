"""Módulo 2 - Práctica 2, parte B: calculadora de nómina."""

# Nota: Intentado primero por mi cuenta y revisado con apoyo de IA para corregir fallos y mejorar el estilo.

SEGURIDAD_SOCIAL = 6.35
PAGAS = 12

TRAMOS_IRPF = [
    (12450, 0.19),
    (20200, 0.24),
    (35200, 0.30),
    (60000, 0.37),
    (300000, 0.45),
    (float("inf"), 0.47),
]


def calcular_irpf(bruto_anual: float) -> float:
    """Calcula la retención anual de IRPF con una escala progresiva.

    Cada tramo se aplica solo a la parte del salario que cae dentro de él.

    >>> calcular_irpf(30000)
    7165.5
    """
    if bruto_anual <= 0:
        return 0.0

    impuesto = 0.0
    limite_inferior = 0.0

    for limite_superior, tipo in TRAMOS_IRPF:
        if bruto_anual <= limite_inferior:
            break
        base_tramo = min(bruto_anual, limite_superior) - limite_inferior
        impuesto += base_tramo * tipo
        limite_inferior = limite_superior

    return round(impuesto, 2)


def calcular_seguridad_social(bruto_anual: float) -> float:
    """Calcula la cotización anual del trabajador a la Seguridad Social.

    >>> calcular_seguridad_social(30000)
    1905.0
    """
    if bruto_anual <= 0:
        return 0.0
    return round(bruto_anual * SEGURIDAD_SOCIAL / 100, 2)


def calcular_neto_anual(bruto_anual: float) -> float:
    """Devuelve el salario neto anual: bruto menos IRPF y Seguridad Social.

    >>> calcular_neto_anual(30000)
    20929.5
    """
    irpf = calcular_irpf(bruto_anual)
    ss = calcular_seguridad_social(bruto_anual)
    return round(bruto_anual - irpf - ss, 2)


def tipo_efectivo(bruto_anual: float) -> float:
    """Devuelve el porcentaje de IRPF sobre el bruto, con dos decimales.

    Si el bruto es cero o negativo devuelve 0.0.

    >>> tipo_efectivo(30000)
    23.89
    """
    if bruto_anual <= 0:
        return 0.0
    return round(calcular_irpf(bruto_anual) / bruto_anual * 100, 2)


def formatear_nomina(bruto_anual: float) -> str:
    """Devuelve el resumen de la nómina en cinco líneas alineadas.

    >>> print(formatear_nomina(30000))
    Bruto anual            30,000.00
    IRPF (23.89 %)         -7,165.50
    Seguridad Social       -1,905.00
    Neto anual             20,929.50
    Neto mensual            1,744.12
    """
    irpf = calcular_irpf(bruto_anual)
    ss = calcular_seguridad_social(bruto_anual)
    neto_anual = calcular_neto_anual(bruto_anual)
    neto_mensual = neto_anual / PAGAS
    tipo = tipo_efectivo(bruto_anual)

    irpf_mostrar = -irpf if irpf else 0.0
    ss_mostrar = -ss if ss else 0.0

    lineas = [
        f"{'Bruto anual':<20}{bruto_anual:>12,.2f}",
        f"{f'IRPF ({tipo:.2f} %)':<20}{irpf_mostrar:>12,.2f}",
        f"{'Seguridad Social':<20}{ss_mostrar:>12,.2f}",
        f"{'Neto anual':<20}{neto_anual:>12,.2f}",
        f"{'Neto mensual':<20}{neto_mensual:>12,.2f}",
    ]
    return "\n".join(lineas)


def main() -> None:
    """Pide el salario bruto anual y muestra la nómina."""
    entrada = input("Introduce el salario bruto anual (€): ").strip()
    try:
        bruto = float(entrada)
    except ValueError:
        print("Importe no válido.")
        return

    if bruto < 0:
        print("Importe no válido.")
        return

    print(formatear_nomina(bruto))

if __name__ == "__main__":
    main()