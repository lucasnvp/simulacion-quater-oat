# Datos
VENTAS_DIARIAS
DEMORA_PROVEEDOR
DESPERFECTO_EQUIPO_DE_EMPAQUETADO
AUSENCIA_EMPREADOS
PESTE_EN_STOCK

# Control
STOCK_AVENA
CANT_OPERARIOS

# Resultados
PROMEDIO_ANUAL_DE_VENTAS
PORCENTAJE_VENTAS_PERDIDAS
PORCENTAJE_DE_PERDIDA_DEL_STOCK_POR_PESTE
BENEFICIO

# Estado
STOCK_AVENA
STOCK_AVENA_EMPAQUETADA

# TEF
FECHA_LLEGADA_PEDIDO


main()
  pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()

    try:
        main()
    except Exception as e:
        logger.exception(e)
