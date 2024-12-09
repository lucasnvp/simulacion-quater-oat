import random

# Datos
def ventas_diarias():
    return random.randint(30, 40)


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
    return random.randint(30, 50)
