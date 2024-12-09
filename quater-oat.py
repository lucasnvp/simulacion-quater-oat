import argparse
import math

from datos import *

# Control
STOCK_REPOSICION_AVENA = 18000  # Cuando el stock de avena llega a 10 se realiza un pedido
CANT_OPERARIOS = 4
# Valores fijos
TP = 28000 # TP: Tamaño de Pedido (Kg)
VALOR_PAQUETE_1KG = 2800 # Entre 2800 y 3700 pesos x kg
COSTO_KILO_AVENA = 780

def llegada_de_pedido(estados):
    estados['stock_avena'] += TP


def empaquetado(estados):
    if desperfecto_equipo_de_empaquetado():
        estados['dia_empaquetado_perdido_x_maquina'] += 1
        return  # No se empaqueta

    if estados['stock_avena'] == 0:
        estados['dia_empaquetado_perdido_x_stock'] += 1
        return

    operarios = 0
    for i in range(CANT_OPERARIOS):
        if not ausencia_empleado():
            operarios += 1
    paquetes = paquetes_por_dia() * operarios
    kg_empaquetados = paquetes * 1
    
    if estados['stock_avena'] < kg_empaquetados:
        estados['stock_avena_empaquetada'] += estados['stock_avena']
        estados['stock_avena'] = 0
    else:
        estados['stock_avena_empaquetada'] += paquetes
        estados['stock_avena'] -= kg_empaquetados


def ventas(estados):
    if estados['stock_avena_empaquetada'] == 0:
        estados['venta_perdida_por_falta_de_paquetes'] += 1
        return

    VD = ventas_diarias()

    if estados['stock_avena_empaquetada'] > VD:
        estados['ventas_totales'] += VD
        estados['beneficio'] += VD * VALOR_PAQUETE_1KG
        estados['stock_avena_empaquetada'] -= VD
    else:
        estados['ventas_totales'] += estados['stock_avena_empaquetada']
        estados['beneficio'] += estados['stock_avena_empaquetada'] * VALOR_PAQUETE_1KG
        estados['stock_avena_empaquetada'] = 0


def generar_orden_de_compra(t, estados):
    demora = demora_proveedor()
    estados['fecha_llegada_pedido'] = t + demora
    estados['beneficio'] -= TP * COSTO_KILO_AVENA
    estados['ordenes_de_compra'] += 1

# Control sobre los paquetes de 1kg
def control_pestes_y_calidad(estados):
    for i in range(estados['stock_avena_empaquetada']):
        if peste_en_avena():
            estados['stock_avena_empaquetada'] -= 1
            estados['kilos_descartados'] += 1


def main(iterations: int):
    print("Quater Oat")
    print(f"Iteracions: {iterations} \n")
    print(f"STOCK_REPOSICION_AVENA: {STOCK_REPOSICION_AVENA}")
    print(f"CANT_OPERARIOS: {CANT_OPERARIOS} \n")

    estados = {
        'stock_avena': 0,
        'stock_avena_empaquetada': 0,
        'fecha_llegada_pedido': 0,
        'beneficio': 0,
        'ventas_totales': 0,
        'ordenes_de_compra': 0,
        'venta_perdida_por_falta_de_paquetes': 0,
        'dia_empaquetado_perdido_x_stock': 0,
        'dia_empaquetado_perdido_x_maquina': 0,
        'kilos_descartados': 0,
    }

    for t in range(iterations):
        # Llegada de pedido
        if t == estados['fecha_llegada_pedido']:
            llegada_de_pedido(estados)

        if t % 7 == 0:
            control_pestes_y_calidad(estados)
        empaquetado(estados)
        ventas(estados)

        if estados['stock_avena'] <= STOCK_REPOSICION_AVENA and estados['fecha_llegada_pedido'] < t:
            generar_orden_de_compra(t, estados)


    # Resultados
    print("VENTAS", estados['ventas_totales'])
    print("STOCK_AVENA", estados['stock_avena'])
    print(f"STOCK_AVENA_EMPAQUETADA: {estados['stock_avena_empaquetada']}")
    kg_totales = estados['ordenes_de_compra'] * TP
    print(f"ORDENES_DE_COMPRA: {estados['ordenes_de_compra']} ({kg_totales} kg)")
    print(f"DIA_EMPAQUETADO_PERDIDO_X_FALTA_ST: {estados['dia_empaquetado_perdido_x_stock']} ({round((estados['dia_empaquetado_perdido_x_stock']/iterations)*100,2)}%)")
    print(f"DIA_EMPAQUETADO_PERDIDO_X_MAQUINA: {estados['dia_empaquetado_perdido_x_maquina']} ({round((estados['dia_empaquetado_perdido_x_maquina']/iterations)*100,2)}%)")
    print(f"VENTA_PERDIDA_POR_FALTA_DE_PAQUETES: {estados['venta_perdida_por_falta_de_paquetes']} ({round((estados['venta_perdida_por_falta_de_paquetes']/estados['ventas_totales'])*100,2)}%)")
    # print("PROMEDIO_ANUAL_DE_VENTAS", PROMEDIO_ANUAL_DE_VENTAS)
    # print("PORCENTAJE_VENTAS_PERDIDAS", PORCENTAJE_VENTAS_PERDIDAS)
    print(f"KILOS_DESCARTADOS: {estados['kilos_descartados']} ({round((estados['kilos_descartados']/kg_totales)*100,2)}%)")
    # print("PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE", PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE)
    print(f"BENEFICIO: {estados['beneficio']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', default=365, type=int)
    args = parser.parse_args()

    main(iterations=args.iteration)
