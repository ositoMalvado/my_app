def calcular_alto(ancho=None, alto=None):
    # Relación de aspecto 16:9
    relacion_aspecto = 16 / 9
    # Calcular el alto correspondiente
    if ancho is not None:
        alto = ancho * relacion_aspecto
    elif alto is not None:
        ancho = alto / relacion_aspecto
    return ancho, alto
