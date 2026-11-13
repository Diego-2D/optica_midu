"""Controlador para la lógica de ventas, abonos y estatus de entrega."""

from database import db_manager
from models.venta import Venta


def registrar_venta(
    paciente_id,
    tipo_lente,
    tratamiento,
    diseno_progresivo,
    calidad_armazon,
    total,
    anticipo=0.0,
    estatus_entrega="En Proceso",
):
    """Valida datos comerciales, calcula saldo y registra la venta."""
    total_val = float(total or 0.0)
    anticipo_val = float(anticipo or 0.0)

    if total_val < 0 or anticipo_val < 0:
        raise ValueError("Los importes no pueden ser negativos.")
    if anticipo_val > total_val:
        raise ValueError("El anticipo no puede ser mayor al total de la venta.")

    # El diseño progresivo solo aplica si el tipo de lente es Progresivo
    diseno_final = (
        diseno_progresivo.strip()
        if tipo_lente and tipo_lente.strip().lower() == "progresivo" and diseno_progresivo
        else None
    )

    saldo_pendiente = round(total_val - anticipo_val, 2)
    estatus_pago = "Liquidado" if saldo_pendiente == 0 else "Pendiente"

    return db_manager.crear_venta(
        paciente_id=paciente_id,
        tipo_lente=tipo_lente,
        tratamiento=tratamiento,
        diseno_progresivo=diseno_final,
        calidad_armazon=calidad_armazon,
        total=total_val,
        anticipo=anticipo_val,
        saldo_pendiente=saldo_pendiente,
        estatus_pago=estatus_pago,
        estatus_entrega=estatus_entrega,
    )


def listar_ventas():
    """Devuelve todas las ventas como objetos Venta."""
    filas = db_manager.obtener_ventas()
    return [Venta.from_db_row(fila) for fila in filas]


def listar_ventas_paciente(paciente_id):
    """Devuelve el historial de ventas de un paciente específico."""
    filas = db_manager.obtener_ventas_por_paciente(paciente_id)
    return [Venta.from_db_row(fila) for fila in filas]


def listar_pendientes_cobranza():
    """Devuelve las ventas con saldo pendiente o sin entregar."""
    filas = db_manager.obtener_ventas_pendientes()
    return [Venta.from_db_row(fila) for fila in filas]


def registrar_abono_o_entrega(venta_id, total, nuevo_anticipo, estatus_entrega):
    """Actualiza el monto pagado, recalcula saldo y actualiza estatus de entrega."""
    total_val = float(total or 0.0)
    anticipo_val = float(nuevo_anticipo or 0.0)

    if anticipo_val > total_val:
        raise ValueError("El monto pagado excede el total de la venta.")

    saldo = round(total_val - anticipo_val, 2)
    estatus_pago = "Liquidado" if saldo == 0 else "Pendiente"

    return db_manager.actualizar_pago_y_entrega(
        venta_id=venta_id,
        anticipo=anticipo_val,
        saldo_pendiente=saldo,
        estatus_pago=estatus_pago,
        estatus_entrega=estatus_entrega,
    )