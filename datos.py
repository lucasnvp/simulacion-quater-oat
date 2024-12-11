import random
import math
from scipy.stats import gamma

"""
FDP de ventas diarias. Se modela como Gamma Distribution por método de la inversa
Docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html
 - alfa: continuous shape parameter (>0)
 - beta: continuous scale parameter (>0)
"""
def ventas_diarias():
    alfa=3.3718
    beta=515.21
    R = random.uniform(0, 1)
    # ppf (percent point function) is a less common name for the inverse of the Cumulative Distribution Function
    return math.floor(gamma.ppf(R, alfa, scale=beta))


def desperfecto_equipo_de_empaquetado():
    # Genera un número aleatorio entre 0 y 1
    probabilidad = random.uniform(0, 1)  # Entre 0 y 1, representa 0% a 100%

    return probabilidad <= 0.01


def ausencia_empleado():
    # Genera un número aleatorio entre 0 y 1
    probabilidad = random.uniform(0, 1)  # Entre 0 y 1, representa 0% a 100%

    # El empleado tiene una probabilidad de 2% a 5% de faltar
    return 0.02 <= probabilidad <= 0.05


def peste_en_avena():
    # Genera un número aleatorio entre 0 y 1
    probabilidad = random.uniform(0, 1)  # Entre 0 y 1, representa 0% a 100%

    # El bolson de avena tiene una probabilidad de 1% a 2% de tener una peste
    return 0.01 <= probabilidad <= 0.02


def demora_proveedor():
    return random.randint(25, 35)


def paquetes_por_dia():
    return random.randint(200, 250)
