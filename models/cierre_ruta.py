"""Modelo de datos para el cierre financiero simple por ruta o fecha."""


class CierreRuta:
    """Representa el balance operativo simple de una campaña o jornada."""

    def __init__(
        self,
        fecha,
        localidad_id=None,
        total_venta=0.0,
        gastos_viaticos=0.0,
        gastos_materiales=0.0,
        gastos_armazones=0.0,
        gastos_maquilas=0.0,
        gastos_accesorios=0.0,
        cierre_id=None,
        localidad_nombre=None,
    ):
        self.id = cierre_id
        self.localidad_id = localidad_id
        self.fecha = fecha
        self.total_venta = float(total_venta or 0.0)
        self.gastos_viaticos = float(gastos_viaticos or 0.0)
        self.gastos_materiales = float(gastos_materiales or 0.0)
        self.gastos_armazones = float(gastos_armazones or 0.0)
        self.gastos_maquilas = float(gastos_maquilas or 0.0)
        self.gastos_accesorios = float(gastos_accesorios or 0.0)
        self.localidad_nombre = localidad_nombre

    @property
    def total_gastos(self):
        """Suma los 5 rubros operativos de gastos."""
        return (
            self.gastos_viaticos
            + self.gastos_materiales
            + self.gastos_armazones
            + self.gastos_maquilas
            + self.gastos_accesorios
        )

    @property
    def utilidad_neta(self):
        """Calcula la ganancia libre descontando todos los gastos."""
        return self.total_venta - self.total_gastos

    @classmethod
    def from_db_row(cls, row):
        """Construye una instancia de CierreRuta desde una fila sqlite3.Row."""
        if not row:
            return None
        keys = row.keys()
        return cls(
            cierre_id=row["id"],
            localidad_id=row["localidad_id"],
            fecha=row["fecha"],
            total_venta=row["total_venta"],
            gastos_viaticos=row["gastos_viaticos"],
            gastos_materiales=row["gastos_materiales"],
            gastos_armazones=row["gastos_armazones"],
            gastos_maquilas=row["gastos_maquilas"],
            gastos_accesorios=row["gastos_accesorios"],
            localidad_nombre=row["localidad_nombre"] if "localidad_nombre" in keys else None,
        )