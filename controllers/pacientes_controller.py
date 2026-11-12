"""Controlador para gedtionar la logica de negocio de los Pacientes"""
from database import db_manager
from models.paciente import Paciente


# ==========================================
# REGISTRO DE PACIENTES
# ==========================================

def registrar_paciente(
nombre,
localidad_id= None,
telefono= "",
edad= None,
graduacion_od= "",
graduacion_oi= "",
presbicia= "",
observaciones= ""):
    """Registra un nuevo Pacienteen la base de datos."""
    if not nombre:
        raise ValueError("El nombre del paciente es obligatorio.")

    paciente_id = db_manager.crear_paciente(
        localidad_id= localidad_id,
        nombre= nombre,
        telefono= telefono,
        edad= edad,
        graduacion_od= graduacion_od,
        graduacion_oi= graduacion_oi,
        presbicia= presbicia,
        observaciones= observaciones
    )
    return paciente_id

# ==========================================
# LISTADOS Y BUSQUEDAS DE PACIENTES
# ==========================================


def listar_pacientes():
    """Obtiene todos los pacientes registrados convertidos a objetos Paciente."""
    filas = db_manager.obtener_pacientes()
    return [Paciente.from_db_row(filas) for fila in filas]

def listar_pacientes_por_localidad(localidad_id):
    """Obtiene los pacientes pertenecientes a una localidad especifica."""
    filas = db_manager.obtener_pacientes_por_localidad(localidad_id)
    return [Paciente.from_db_row(fila) for fila in filas]

def obtener_paciente(paciente_id):
    """Obtiene los pacientes pertenecientes a una localidad especifica."""
    fila = db_manager.obtener_pacientes_por_id(paciente_id)
    return [Paciente.from_db_row(fila)]

def buscar_pacientes_por_nombre(texto_busqueda):
    """Obtiene los pacientes por nombre especifico."""
    filas = db_manager.obtener_pacientes_por_nombre(texto_busqueda)
    return [Paciente.from_db_row(fila) for fila in filas]


# ==========================================
# MODIFICACIÓN Y BORRADO DE PACIENTES
# ==========================================

def modificar_paciente(
        paciente_id,
        nombre,
        telefono,
        edad,
        graduacion_od,
        graduacion_oi,
        presbicia,
        observaciones
):
    """Actualiza los datos clinicos y personales de un paciente"""
    return db_manager.actualizar_paciente(
        paciente_id= paciente_id,
        nombre= nombre,
        telefono= telefono,
        edad= edad,
        graduacion_od= graduacion_od,
        graduacion_oi= graduacion_oi,
        presbicia= presbicia,
        observaciones= observaciones
    )

def borrar_paciente(paciente_id):
    """Elimina de forma permanente un paciente por su ID"""
    return db_manager.eliminar_paciente(paciente_id)