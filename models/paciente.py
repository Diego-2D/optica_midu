"""Modulo de Modelo de Pacientes"""
class Paciente:
    """Representa un Paciente"""

    def __init__(
            self,
            nombre,
            localidad_id=None,
            telefono="",
            edad=None,
            graduacion_od="",
            graduacion_oi="",
            presbicia="",
            observaciones="",
            paciente_id= None):
        
        self.id = paciente_id
        self.nombre = nombre
        self.localidad_id = localidad_id
        self.telefono = telefono
        self.edad = edad
        self.graduacion_od = graduacion_od
        self.graduacion_oi = graduacion_oi
        self.presbicia = presbicia
        self.observaciones = observaciones

    @classmethod
    def from_db_row(cls,row):
        """Transforma un fila devuelta por SQLite en un Objeto Localidad"""
        if row is None:
            return None
        return cls(
            paciente_id = row["id"],
            localidad_id = row["localidad_id"],
            nombre = row["nombre"],
            telefono = row["telefono"],
            edad = row["edad"],
            graduacion_od = row["graduacion_od"],
            graduacion_oi = row["graduacion_oi"],
            presbicia = row["presbicia"],
            observaciones = row["observaciones"]
        )

    def resumen_graduacion_(self):
        """Devuelve un formato detexto rapido con la graduacion clinica."""
        od = self.graduacion_od if self.graduacion_od else "N/A"
        oi = self.graduacion_oi if self.graduacion_oi else "N/A"
        add = self.presbicia if self.presbicia else "N/A"
        return f"OD: {od} | OI: {oi} | ADD: {add}"

    def __repr__(self):
        return f"<Paciente {self.id}: {self.nombre}>"