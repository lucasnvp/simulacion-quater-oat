import argparse
import math

from datos import *

# Control
STOCK_REPOSICION_AVENA = 14000  # Cuando el stock de avena llega a 10 se realiza un pedido
CANT_OPERARIOS = 10
CANTIDAD_COMPRADA = 28000
GANANCIA_PAQUETE_AVENA = 2800   # Entre 2800 y 3700 pesos
COSTO_KILO_AVENA = 780

def llegada_de_pedido(estados):
    estados['stock_avena'] += CANTIDAD_COMPRADA
    estados['beneficio'] -= CANTIDAD_COMPRADA * COSTO_KILO_AVENA
    estados['ordenes_de_compra'] += 1


def empaquetado(estados):
    if desperfecto_equipo_de_empaquetado():
        estados['dia_perdido_por_desperfecto_maquina_empaquetadora'] += 1
        return  # No se empaqueta

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
    if estados['stock_avena_empaquetada'] == 0:
        estados['dia_perdido_por_falta_de_paquetes'] += 1
        return

    ventas = ventas_diarias()
    estados['ventas_totales'] += ventas
    estados['stock_avena_empaquetada'] -= ventas

    if estados['stock_avena_empaquetada'] < 0:
        estados['ventas_totales'] += estados['stock_avena_empaquetada']
        estados['stock_avena_empaquetada'] = 0
        estados['beneficio'] += estados['ventas_totales'] * GANANCIA_PAQUETE_AVENA
    else:
        estados['ventas_totales'] += ventas
        estados['beneficio'] += ventas * GANANCIA_PAQUETE_AVENA


def generar_orden_de_compra(t, estados):
    demora = demora_proveedor()
    estados['fecha_llegada_pedido'] = t + demora


def peste_en_el_stock(estados):
    bolsones = math.ceil(estados['stock_avena'] / 25)  # Redondeo positivo
    for i in range(bolsones):
        if peste_en_avena():
            estados['stock_avena'] -= 25
            estados['beneficio'] -= 25 * COSTO_KILO_AVENA
            estados['kilos_desperdiciados_por_peste'] += 25


def main(iterations: int):
    print("Quater Oat")
    print(f"Iteracions: {iterations} \n")

    estados = {
        'stock_avena': 0,
        'stock_avena_empaquetada': 0,

        'fecha_llegada_pedido': 0,

        'beneficio': 0,
        'ventas_totales': 0,
        'ordenes_de_compra': 0,
        'dia_perdido_por_falta_de_paquetes': 0,
        'dia_perdido_por_falta_de_avena': 0,
        'dia_perdido_por_desperfecto_maquina_empaquetadora': 0,
        'kilos_desperdiciados_por_peste': 0,
    }

    for t in range(iterations):
        # Llegada de pedido
        if t == estados['fecha_llegada_pedido']:
            llegada_de_pedido(estados)

        peste_en_el_stock(estados)
        empaquetado(estados)
        ventas(estados)

        if estados['stock_avena'] <= STOCK_REPOSICION_AVENA and estados['fecha_llegada_pedido'] < t:
            generar_orden_de_compra(t, estados)


    # Resultados
    print("VENTAS", estados['ventas_totales'])
    print("STOCK_AVENA", estados['stock_avena'])
    print(f"STOCK_AVENA_EMPAQUETADA: {estados['stock_avena_empaquetada']}")
    print(f"ORDENES_DE_COMPRA: {estados['ordenes_de_compra']}")
    print(f"DIA_PERDIDO_POR_FALTA_DE_AVENA: {estados['dia_perdido_por_falta_de_avena']}")
    print(f"DIA_PERDIDO_POR_FALTA_DE_PAQUETES: {estados['dia_perdido_por_falta_de_paquetes']}")
    # print("PROMEDIO_ANUAL_DE_VENTAS", PROMEDIO_ANUAL_DE_VENTAS)
    # print("PORCENTAJE_VENTAS_PERDIDAS", PORCENTAJE_VENTAS_PERDIDAS)
    print(f"KILOS_DESPERCIDIADOS_POR_PERSTE: {estados['kilos_desperdiciados_por_peste']}")
    # print("PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE", PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE)
    print(f"BENEFICIO: {estados['beneficio']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', default=365, type=int)
    args = parser.parse_args()

    main(iterations=args.iteration)
