from librodiario import LibroDiario, MontoInvalidoError

libro = LibroDiario()

try:
    libro.agregar_transaccion('18/06/2025', 'Compra de laptop', 780, 'egreso')
    libro.agregar_transaccion('18/06/2025', 'Venta de sensor TK-110', 780, 'ingreso')
    libro.agregar_transaccion('25/06/2025', 'Compra de software', 250, 'egreso')
    libro.agregar_transaccion('18/06/2025', 'Compra de insumos de oficina', 85.60, 'egreso')
except (ValueError, MontoInvalidoError) as e:
    print(f"Error: {e}")

libro.cargar_transacciones_desde_archivo("registro.csv")

print("Resumen contable:")
print(libro.calcular_resumen())
