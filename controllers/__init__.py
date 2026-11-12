"""Paquete de controladores para la aplicación Óptica Midu."""

from controllers.localidades_controller import (
    registrar_localidad,
    listar_localidades,
    modificar_localidad,
    borrar_localidad
)

from controllers.pacientes_controller import (
    registrar_paciente,
    listar_pacientes,
    listar_pacientes_por_localidad,
    obtener_paciente,
    buscar_pacientes_por_nombre,
    modificar_paciente,
    borrar_paciente
)