"""Controlador para el registro y consulta simple de cierres de ruta."""

from datetime import date
from database import db_manager
from models.cierre_ruta import CierreRuta


def registrar_cierre_ruta(
    localidad_id=None,
    fecha=None,
    total_venta=0.0,
    gastos_viaticos=0.0,
    gastos_materiales=0.0,
    gastos_armazones=0.0,
    gastos_maquilas=0.0,
    gastos_accesorios=0.0,
):
    """Registra los totales de venta y gastos operativos de una ruta o fecha."""
    fecha_final = fecha.strip() if fecha and fecha.strip() else date.today().isoformat()

    return db_manager.crear_cierre_ruta(
        localidad_id=localidad_id,
        fecha=fecha_final,
        total_venta=float(total_venta or 0.0),
        gastos_viaticos=float(gastos_viaticos or 0.0),
        gastos_materiales=float(gastos_materiales or 0.0),
        gastos_armazones=float(gastos_armazones or 0.0),
        gastos_maquilas=float(gastos_maquilas or 0.0),
        gastos_accesorios=float(gastos_accesorios or 0.0),
    )


def listar_cierres_ruta():
    """Devuelve todos los cierres financieros registrados como objetos CierreRuta."""
    filas = db_manager.obtener_cierres_ruta()
    return [CierreRuta.from_db_row(fila) for fila in filas]