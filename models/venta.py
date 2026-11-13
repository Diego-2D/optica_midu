"""Modelo de datos para representar las ventas y cobranza de Servicios Ópticos MIDU."""


class Venta:
    """Representa una orden de trabajo / venta vinculada a un paciente."""

    def __init__(
        self,
        paciente_id,
        tipo_lente=None,
        tratamiento=None,
        diseno_progresivo=None,
        calidad_armazon=None,
        total=0.0,
        anticipo=0.0,
        saldo_pendiente=0.0,
        estatus_pago="Pendiente",
        estatus_entrega="En Proceso",
        fecha_venta=None,
        venta_id=None,
        paciente_nombre=None,
        paciente_telefono=None,
    ):
        self.id = venta_id
        self.paciente_id = paciente_id
        self.tipo_lente = tipo_lente
        self.tratamiento = tratamiento
        self.diseno_progresivo = diseno_progresivo
        self.calidad_armazon = calidad_armazon
        self.total = float(total or 0.0)
        self.anticipo = float(anticipo or 0.0)
        self.saldo_pendiente = float(saldo_pendiente or 0.0)
        self.estatus_pago = estatus_pago
        self.estatus_entrega = estatus_entrega
        self.fecha_venta = fecha_venta
        self.paciente_nombre = paciente_nombre
        self.paciente_telefono = paciente_telefono

    def resumen_trabajo(self):
        """Devuelve una descripción técnica limpia del lente y armazón."""
        partes = []
        if self.tipo_lente:
            lente = self.tipo_lente
            if self.tipo_lente.lower() == "progresivo" and self.diseno_progresivo:
                lente += f" ({self.diseno_progresivo})"
            partes.append(lente)
        if self.tratamiento:
            partes.append(self.tratamiento)
        if self.calidad_armazon:
            partes.append(f"Armazón: {self.calidad_armazon}")

        return " | ".join(partes) if partes else "Sin especificaciones ópticas"

    @classmethod
    def from_db_row(cls, row):
        """Construye una instancia de Venta desde una fila sqlite3.Row."""
        if not row:
            return None
        keys = row.keys()
        return cls(
            venta_id=row["id"],
            paciente_id=row["paciente_id"],
            tipo_lente=row["tipo_lente"],
            tratamiento=row["tratamiento"],
            diseno_progresivo=row["diseno_progresivo"],
            calidad_armazon=row["calidad_armazon"],
            total=row["total"],
            anticipo=row["anticipo"],
            saldo_pendiente=row["saldo_pendiente"],
            estatus_pago=row["estatus_pago"],
            estatus_entrega=row["estatus_entrega"],
            fecha_venta=row["fecha_venta"],
            paciente_nombre=row["paciente_nombre"] if "paciente_nombre" in keys else None,
            paciente_telefono=row["paciente_telefono"] if "paciente_telefono" in keys else None,
        )