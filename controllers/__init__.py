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

from controllers.ventas_controller import (
    registrar_venta,
    listar_ventas,
    listar_ventas_paciente,
    listar_pendientes_cobranza,
    registrar_abono_o_entrega,
)
from controllers.finanzas_controller import (
    registrar_cierre_ruta,
    listar_cierres_ruta,
)