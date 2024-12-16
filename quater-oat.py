import argparse

from datos import *

# Valores fijos
VALOR_PAQUETE_1KG = 2800 # Entre 2800 y 3700 pesos x kg
COSTO_KILO_AVENA = 780


def llegada_de_pedido(estados, tp):
    estados['stock_avena'] += tp


def empaquetado(dia_simulacion, estados, cant_operarios):
    if desperfecto_equipo_de_empaquetado():
        estados['dia_empaquetado_perdido_x_maquina'] += 1
        return  # No se empaqueta

    if estados['stock_avena'] == 0:
        estados['dia_empaquetado_perdido_x_stock'] += 1
        return

    operarios = 0
    for i in range(cant_operarios):
        if not ausencia_empleado(dia_simulacion):
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
        estados['venta_parcialmente_perdida_por_falta_de_paquetes'] += 1
        estados['stock_avena_empaquetada'] = 0


def generar_orden_de_compra(t, estados, tp):
    demora = demora_proveedor()
    estados['fecha_llegada_pedido'] = t + demora
    estados['beneficio'] -= (tp * COSTO_KILO_AVENA)
    estados['ordenes_de_compra'] += 1


def control_pestes_y_calidad(estados):
    # Control sobre los paquetes de 1 kg
    for i in range(estados['stock_avena_empaquetada']):
        if peste_en_avena():
            estados['stock_avena_empaquetada'] -= 1
            estados['kilos_descartados'] += 1
    # Control sobre los bolsones de 25 kg
    for i in range(math.floor(estados['stock_avena']/25)):
        if peste_en_avena():
            estados['stock_avena'] -= 25
            estados['kilos_descartados'] += 25


def main(iterations: int, cant_operarios: int, stock_reposicion_avena: int, tp: int):
    print("Quater Oat")
    print(f"Iteracions: {iterations} \n")
    print(f"STOCK_REPOSICION_AVENA: {stock_reposicion_avena}")
    print(f"CANT_OPERARIOS: {cant_operarios} \n")

    estados = {
        'stock_avena': 0,
        'stock_avena_empaquetada': 0,
        'fecha_llegada_pedido': 0,
        'beneficio': 0,
        'ventas_totales': 0,
        'ordenes_de_compra': 0,
        'venta_perdida_por_falta_de_paquetes': 0,
        'venta_parcialmente_perdida_por_falta_de_paquetes': 0,
        'dia_empaquetado_perdido_x_stock': 0,
        'dia_empaquetado_perdido_x_maquina': 0,
        'kilos_descartados': 0,
    }

    for t in range(iterations):
        # Llegada de pedido
        if t == estados['fecha_llegada_pedido']:
            llegada_de_pedido(estados, tp)

        if t % 7 == 0:
            control_pestes_y_calidad(estados)
        empaquetado(t, estados, cant_operarios)
        ventas(estados)

        if estados['stock_avena'] <= stock_reposicion_avena and estados['fecha_llegada_pedido'] < t:
            generar_orden_de_compra(t, estados, tp)


    # Resultados
    print("VENTAS", estados['ventas_totales'])
    print(f"PROMEDIO_ANUAL_DE_VENTAS: {round((estados['ventas_totales']/(iterations/365)), 2)}")
    print("STOCK_AVENA", estados['stock_avena'])
    print(f"STOCK_AVENA_EMPAQUETADA: {estados['stock_avena_empaquetada']}")
    kg_totales = estados['ordenes_de_compra'] * tp
    print(f"ORDENES_DE_COMPRA: {estados['ordenes_de_compra']} ({kg_totales} kg)")
    print(f"ORDENES_DE_COMPRA_ANUALES: {estados['ordenes_de_compra']/(iterations/365)}")
    print(f"DIA_EMPAQUETADO_PERDIDO_X_FALTA_ST: {estados['dia_empaquetado_perdido_x_stock']} ({round((estados['dia_empaquetado_perdido_x_stock']/iterations)*100,2)}%)")
    print(f"DIA_EMPAQUETADO_PERDIDO_X_MAQUINA: {estados['dia_empaquetado_perdido_x_maquina']} ({round((estados['dia_empaquetado_perdido_x_maquina']/iterations)*100,2)}%)")
    print(f"VENTA_PERDIDA_POR_FALTA_DE_PAQUETES: {estados['venta_perdida_por_falta_de_paquetes']} ({round((estados['venta_perdida_por_falta_de_paquetes']/iterations)*100,2)}%)")
    print(f"VENTA_PARCIALMENTE_PERDIDA_POR_FALTA_DE_PAQUETES: {estados['venta_parcialmente_perdida_por_falta_de_paquetes']} ({round((estados['venta_parcialmente_perdida_por_falta_de_paquetes']/iterations)*100,2)}%)")
    print(f"KILOS_DESCARTADOS: {estados['kilos_descartados']} ({round((estados['kilos_descartados']/kg_totales)*100,2)}%)")
    print(f"BENEFICIO: {estados['beneficio']}")
    print(f"BENEFICIO_ANUALIZADO: {round((estados['beneficio']/(iterations/365)), 2)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--iteration', default=365, type=int)
    parser.add_argument('--cant_operarios', default=4, type=int)
    parser.add_argument('--stock_reposicion_avena', default=18000, type=int)  # Cuando el stock de avena llega a este valor se realiza un pedido
    parser.add_argument('--tp', default=28000, type=int)  # Tamaño del pedido

    args = parser.parse_args()

    main(
        iterations=args.iteration,
        cant_operarios=args.cant_operarios,
        stock_reposicion_avena=args.stock_reposicion_avena,
        tp=args.tp
    )
