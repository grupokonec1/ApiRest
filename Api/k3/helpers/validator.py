import re

def calcular_dv_chile(rut: str) -> str:
    reversed_digits = list(map(int, reversed(rut)))
    factors = [2, 3, 4, 5, 6, 7]
    total = sum(d * factors[i % 6] for i, d in enumerate(reversed_digits))
    remainder = 11 - (total % 11)
    if remainder == 11:
        return '0'
    elif remainder == 10:
        return 'K'
    else:
        return str(remainder)
    
def procesar_rut_desde_texto(mensaje: str) -> str:
    """
    Extrae los números desde un mensaje con texto libre, calcula el DV si es necesario,
    y retorna el RUT en formato correcto.
    """
    # Elimina puntos y espacios
    limpio = re.sub(r'[.\s]', '', mensaje.upper())

    # Busca secuencia de al menos 6 a 8 dígitos consecutivos
    match = re.search(r'(\d{6,8})(?:-?([0-9K]))?', limpio)
    if not match:
        raise ValueError("No se encontró un RUT válido en el mensaje.")

    cuerpo = match.group(1)
    dv = match.group(2)

    if not dv:
        dv = calcular_dv_chile(cuerpo)

    return f"{cuerpo}-{dv}"