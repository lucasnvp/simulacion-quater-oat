import random
import math
from scipy.stats import gamma
import numpy as np


"""
FDP de ventas diarias. Se modela como Gamma Distribution por método de la inversa
Docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html
 - alfa: continuous shape parameter (>0)
 - beta: continuous scale parameter (>0)
"""
def ventas_diarias():
    alfa=3.3648
    beta=206.4
    R = random.uniform(0, 1)
    # ppf (percent point function) is a less common name for the inverse of the Cumulative Distribution Function
    return math.floor(gamma.ppf(R, alfa, scale=beta))


def desperfecto_equipo_de_empaquetado():
    # Genera un número aleatorio entre 0 y 1
    probabilidad = random.uniform(0, 1)  # Entre 0 y 1, representa 0% a 100%

    # Genera un número aleatorio entre 0% y 2%
    probabilidad_de_peste = random.uniform(0, 0.02)

    return probabilidad <= probabilidad_de_peste


def ausencia_empleado(dia_simulacion):
    # Rangos de mayor probabilidad de enfermedad, del 15 de junio al 15 de agosto
    INICIO_RANGO_INV = 165
    FIN_RANGO_INV = 227

    dia_actual = dia_simulacion % 365
    es_invierno = INICIO_RANGO_INV <= dia_actual <= FIN_RANGO_INV

    # Probabilidad de ausencia según la estación
    probabilidad_ausencia = 0.1 if es_invierno else 0.02

    # Genera un número aleatorio entre 0 y 1
    probabilidad = random.uniform(0, 1)

    return probabilidad < probabilidad_ausencia


def peste_en_avena(tasa_peste=0.01):
    """Simula la aparición de una peste utilizando la distribución exponencial.

    Args:
        tasa_peste (float): Tasa de ocurrencia de la peste (por ejemplo, 0.01 = peste cada 100 días en promedio).

    Returns:
        bool: Indica si hubo peste o no.
    """

    # Cuándo ocurre la peste (esperar un tiempo hasta la próxima peste)
    tiempo_espera_peste = np.random.exponential(1 / tasa_peste)  # Tiempo de espera para la siguiente peste
    peste_ocurre = tiempo_espera_peste < 1  # La peste ocurre dentro del día si el tiempo de espera es menor a 1 día

    return peste_ocurre


"""
FDP de demora_proveedor. Se modela como Gamma Distribution por método de la inversa
Docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html
 - alfa: continuous shape parameter (>0)
 - beta: continuous scale parameter (>0)
Devuelve valores aproximadamente entre 25 y 35
"""
def demora_proveedor():
    alfa=133.38
    beta=0.21101
    R = random.uniform(0, 1)
    # ppf (percent point function) is a less common name for the inverse of the Cumulative Distribution Function
    return math.floor(gamma.ppf(R, alfa, scale=beta))

def paquetes_por_dia():
    return random.randint(200, 250)
