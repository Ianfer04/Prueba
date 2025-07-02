import logging
from datetime import datetime
from typing import List, Dict

# Configuración de logging
logging.basicConfig(
    filename="log_contable.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


class MontoInvalidoError(Exception):
    """Excepción para montos inválidos."""


class LibroDiario:
    """Gestión ingresos y egresos."""

    def __init__(self):
        """Inicia la lista de transacciones."""
        self.transacciones: List[Dict] = []

    def agregar_transaccion(self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """
        Agrega una transacción válida al libro diario.

        :param fecha: Fecha en formato 'dd/mm/yyyy'
        :param descripcion: Descripción de la transacción
        :param monto: Monto positivo
        :param tipo: 'ingreso' o 'egreso'
        """
        tipo = tipo.lower()
        if tipo not in ("ingreso", "egreso"):
            logging.error("Tipo inválido: %s", tipo)
            raise ValueError(f"Tipo de transacción inválido ({tipo}). Use 'ingreso' o 'egreso'.")

        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError as exc:
            logging.error("Fecha inválida: %s", fecha)
            raise ValueError(f"Formato de fecha inválido ({fecha}). Use 'dd/mm/yyyy'.") from exc

        if monto < 0:
            logging.error("Monto negativo: %s", monto)
            raise ValueError(f"Monto inválido ({monto}). Debe ser mayor o igual a 0.")

        transaccion = {
            "fecha": datetime.strptime(fecha, "%d/%m/%Y"),
            "descripcion": descripcion,
            "monto": monto,
            "tipo": tipo
        }
        self.transacciones.append(transaccion)
        logging.info("Transacción agregada: %s - %.2f - %s", descripcion, monto, tipo)

    def calcular_resumen(self) -> Dict[str, float]:
        """
        Calcula el total de ingresos y egresos.

        :return: Diccionario con claves 'ingresos' y 'egresos'
        """
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            elif transaccion["tipo"] == "egreso":
                resumen["egresos"] += transaccion["monto"]
        return resumen

    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        """
        Carga transacciones desde un archivo CSV con formato:
        Y-M-D;descripcion;monto;tipo

        :param path: Ruta al archivo
        """
        try:
            with open(path, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(";")
                    if len(datos) != 4:
                        logging.error("Línea inválida: %s", linea.strip())
                        continue

                    fecha, descripcion, valor, tipo = datos
                    try:
                        monto = float(valor)
                    except ValueError:
                        logging.error("Monto inválido: %s", valor)
                        continue

                    try:
                        self.agregar_transaccion(
                            self.convertir_fecha(fecha),
                            descripcion,
                            monto,
                            tipo
                        )
                    except ValueError as exc:
                        logging.warning("Error al agregar transacción: %s", exc)

        except FileNotFoundError as exc:
            logging.critical("Archivo no encontrado: %s", path)
            raise exc

    def convertir_fecha(self, fecha: str) -> str:
        """
        Convierte una fecha de 'Y-M-D' a 'D/M/Y'.

        :param fecha: Fecha en formato ISO
        :return: Fecha en formato latino
        """
        partes = fecha.split("-")
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
