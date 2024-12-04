import argparse

from datos import *

# Control
STOCK_REPOSICION_AVENA = 10  # Cuando el stock de avena llega a 10 se realiza un pedido
CANT_OPERARIOS = 10
CANTIDAD_COMPRADA = 28000


def llegada_de_pedido():
    pass


def empaquetado(estados):
    # todo desperfecto de la maquina de empaquetado

    if estados['stock_avena'] == 0:
        estados['dia_perdido_por_falta_de_avena'] += 1
        return

    paquetes = paquetes_por_dia() * CANT_OPERARIOS
    estados['stock_avena_empaquetada'] += paquetes

    estados['stock_avena'] -= paquetes
    if estados['stock_avena'] < 0:
        estados['stock_avena'] = 0


# def ventas(ventas_totales, stock_avena_empaquetada, dia_perdido_por_falta_de_avena):
def ventas(estados):
    # resultados['ventas_totales'] += 1

    if estados['stock_avena_empaquetada'] == 0:
        estados['dia_perdido_por_falta_de_paquetes'] += 1
        return

    ventas = ventas_diarias()
    estados['ventas_totales'] += ventas
    estados['stock_avena_empaquetada'] -= ventas

    if estados['stock_avena_empaquetada'] < 0:
        estados['ventas_totales'] += estados['stock_avena_empaquetada']
        estados['stock_avena_empaquetada'] = 0
    else:
        estados['ventas_totales'] += ventas


def main(iterations: int):
    print("Quater Oat")
    print("Iterations:", iterations)

    estados = {
        'stock_avena': 28000,
        'stock_avena_empaquetada': 28000,

        'fecha_llegada_pedido': 10000000000,

        'ventas_totales': 0,
        'dia_perdido_por_falta_de_paquetes': 0,
        'dia_perdido_por_falta_de_avena': 0
    }

    for i in range(iterations):
        # Llegada de pedido
        if i == estados['fecha_llegada_pedido']:
            llegada_de_pedido()

        empaquetado(estados)
        ventas(estados)
        # contro_de_stock()


    # Resultados
    print("VENTAS", estados['ventas_totales'])
    print("STOCK_AVENA", estados['stock_avena'])
    print(f"STOCK_AVENA_EMPAQUETADA: {estados['stock_avena_empaquetada']}")
    print(f"DIA_PERDIDO_POR_FALTA_DE_AVENA: {estados['dia_perdido_por_falta_de_avena']}")
    print(f"DIA_PERDIDO_POR_FALTA_DE_PAQUETES: {estados['dia_perdido_por_falta_de_paquetes']}")
    # print("PROMEDIO_ANUAL_DE_VENTAS", PROMEDIO_ANUAL_DE_VENTAS)
    # print("PORCENTAJE_VENTAS_PERDIDAS", PORCENTAJE_VENTAS_PERDIDAS)
    # print("PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE", PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE)
    # print("BENEFICIO", BENEFICIO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', default=365, type=int)
    args = parser.parse_args()

    main(iterations=args.iteration)
