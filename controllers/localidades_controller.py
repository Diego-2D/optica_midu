"""Controlador para gestionar la lógica de negocío de las localides"""
from database import db_manager
from models.localidad import Localidad

def registrar_localidad (nombre, ubicacion, fecha_inicio=None, fecha_fin=None, presupuesto=0.0):
    """Crea una nueva localidad y la guarda en la base de datos"""
    if not nombre or not ubicacion:
        raise ValueError("El nombre y la Ubicacón de la Localidad son obligatorios.")

    localidad_id = db_manager.crear_localidad(
        nombre = nombre,
        ubicacion = ubicacion,
        fecha_inicio = fecha_inicio,
        fecha_fin= fecha_fin,
        presupuesto= presupuesto
    )
    return localidad_id

def listar_localidades():
    """Obtiene todas las localidades registradas convertidas a objetos Localidad"""
    filas = db_manager.obtener_localidades()
    return [Localidad.from_db_row(fila) for fila in filas]

# pylint: disable=too-many-arguments
def modificar_localidad(
localidad_id,
nombre,
ubicacion,
fecha_inicio,
fecha_fin,
presupuesto,
estado):
    """Actualiza los datos de una localidad existente"""
    return db_manager.actualizar_localidad(
        localidad_id= localidad_id,
        nombre= nombre,
        ubicacion= ubicacion,
        fecha_inicio= fecha_inicio,
        fecha_fin= fecha_fin,
        presupuesto= presupuesto,
        estado= estado
    )

def borrar_localidad(localidad_id):
    """Elimina una localidad por su ID"""
    return db_manager.eliminar_localidad(localidad_id)
