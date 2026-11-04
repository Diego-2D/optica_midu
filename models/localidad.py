"""Modulo de modelo para Localidades"""
class Localidad:
    """Representa una Campaña"""
    def __init__(self,
                 nombre,
                 ubicacion,
                 fecha_inicio,
                 fecha_fin=None,
                 presupuesto=0.0,
                 estado="Planificada",
                 localidad_id=None):
        self.id = localidad_id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto = presupuesto
        self.estado = estado

    @classmethod
    def from_db_row(cls,row):
        """Transforma un fila devuelta por SQLite en un Objeto Localidad"""
        if row is None:
            return None
        return cls(
            localidad_id = row["id"],
            nombre = row["nombre"],
            ubicacion = row["ubicacion"],
            fecha_inicio = row["fecha_inicio"],
            fecha_fin = row["fecha_fin"],
            presupuesto = row["presupuesto"],
            estado = row["estado"]
        )

    def to_dict(self):
        """Convierte el objeto en un Diccionario de Python."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "presupuesto": self.presupuesto,
            "estado": self.estado
        }

    def __repr__(self):
        return f"<Localidad {self.id}: {self.nombre} {self.ubicacion}>"