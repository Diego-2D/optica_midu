"""Este archivo es para las Operaciones CRUD: Localidades"""
from database.connection import get_connection


# ==========================================
# OPERACIONES CRUD: LOCALIDADES
# ==========================================

# ==========================================
# ACTUALIZAR LOCALIDADES
# ==========================================

def crear_localidad(nombre, ubicacion, fecha_inicio=None, fecha_fin=None, presupuesto=0.0):
    """Inserta una nueva localidad/campaña en la base de datos."""
    sql = """
        INSERT INTO localidades (nombre, ubicacion, fecha_inicio, fecha_fin, presupuesto)
        VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, ubicacion, fecha_inicio, fecha_fin, presupuesto))
        conn.commit()
        return cursor.lastrowid


# ==========================================
# LEER LOCALIDADES
# ==========================================

def obtener_localidades():
    """Devuelve la lista completa de localidades registradas."""
    sql = "SELECT * FROM localidades ORDER BY id DESC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


# ==========================================
# UPDATE LOCALIDADES
# ==========================================

def actualizar_localidad(localidad_id, nombre, ubicacion, fecha_inicio, fecha_fin, presupuesto, estado):
    """Actualiza los datos de una localidad/campaña existente."""
    sql = """
        UPDATE localidades
        SET nombre = ?,
            ubicacion = ?,
            fecha_inicio = ?,
            fecha_fin = ?,
            presupuesto = ?,
            estado = ?
        WHERE id = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, ubicacion, fecha_inicio, fecha_fin, presupuesto, estado, localidad_id))
        conn.commit()
        return cursor.rowcount > 0

# ==========================================
# BORRAR LOCALIDADES
# ==========================================

def eliminar_localidad(localidad_id):
    """Elimina una localidad por su ID."""
    sql = "DELETE FROM localidades WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (localidad_id,))
        conn.commit()
        return cursor.rowcount > 0



# ==========================================
# OPERACIONES CRUD: PACIENTES
# ==========================================

# ==========================================
# CREAR PACIENTES
# ==========================================

def crear_paciente(localidad_id, nombre, telefono="", edad=None, graduacion_od="", graduacion_oi="", presbicia="", observaciones=""):
    """Registra un nuevo paciente asociado a una localidad."""
    sql = """
        INSERT INTO pacientes (
            localidad_id, nombre, telefono, edad, 
            graduacion_od, graduacion_oi, presbicia, observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (
            localidad_id, nombre, telefono, edad, 
            graduacion_od, graduacion_oi, presbicia, observaciones
        ))
        conn.commit()
        return cursor.lastrowid


# ==========================================
# LEER PACIENTES
# ==========================================

def obtener_pacientes():
    """Devuelve todos los pacientes  de todas las localidades."""
    sql = """
    SELECT 
        id,
        localidad_id,
        nombre,
        telefono,
        edad,
        graduacion_od,
        graduacion_oi,
        presbicia,
        observaciones

    FROM pacientes
    ORDER BY nombre ASC;
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def obtener_pacientes_por_localidad(localidad_id):
    """Devuelve todos los pacientes atendidos en una localidad específica."""
    sql = "SELECT * FROM pacientes WHERE localidad_id = ? ORDER BY nombre ASC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (localidad_id,))
        return cursor.fetchall()


def obtener_pacientes_por_id(paciente_id):
    """Devuelve el expediente clinico de un paciente unico por su ID."""
    sql = """
    SELECT
        id,
        localidad_id,
        nombre,
        telefono,
        edad,
        graduacion_od,
        graduacion_oi,
        presbicia,
        observaciones
    FROM pacientes
    WHERE id = ?;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (paciente_id,))
        return cursor.fetchall()

def obtener_pacientes_por_nombre(texto_busqueda):
    """Devuelve el expediente clinico de un paciente unico por su nombre."""
    sql = """
    SELECT
        id,
        localidad_id,
        nombre,
        telefono,
        edad,
        graduacion_od,
        graduacion_oi,
        presbicia,
        observaciones
    FROM pacientes
    WHERE nombre LIKE ?
    ORDER BY nombre ASC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (f"%{texto_busqueda}",))
        return cursor.fetchall()



# ==========================================
# ACTUALIZAR PACIENTES
# ==========================================

def actualizar_paciente(paciente_id, nombre, telefono, edad, graduacion_od, graduacion_oi, presbicia, observaciones):
    """Actualiza la información clínica y de contacto de un paciente existente."""
    sql = """
        UPDATE pacientes
        SET nombre = ?,
            telefono = ?,
            edad = ?,
            graduacion_od = ?,
            graduacion_oi = ?,
            presbicia = ?,
            observaciones = ?
        WHERE id = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (
            nombre, telefono, edad, 
            graduacion_od, graduacion_oi, presbicia, 
            observaciones, paciente_id
        ))
        conn.commit()
        return cursor.rowcount > 0  # Devuelve True si se modificó alguna fila

# ==========================================
# ELIMINAR PACIENTES
# ==========================================

def eliminar_paciente(paciente_id):
    """Elimina permanentemente a un paciente por su ID."""
    sql = "DELETE FROM pacientes WHERE id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (paciente_id,))
        conn.commit()
        return cursor.rowcount > 0

# =====================================================================
# GESTIÓN DE VENTAS Y COBRANZA
# =====================================================================

def crear_venta(
    paciente_id,
    tipo_lente,
    tratamiento,
    diseno_progresivo,
    calidad_armazon,
    total,
    anticipo=0.0,
    saldo_pendiente=0.0,
    estatus_pago="Pendiente",
    estatus_entrega="En Proceso",
):
    """Registra una nueva venta vinculada a un paciente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ventas (
            paciente_id, tipo_lente, tratamiento, diseno_progresivo,
            calidad_armazon, total, anticipo, saldo_pendiente,
            estatus_pago, estatus_entrega
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paciente_id,
            tipo_lente,
            tratamiento,
            diseno_progresivo,
            calidad_armazon,
            total,
            anticipo,
            saldo_pendiente,
            estatus_pago,
            estatus_entrega,
        ),
    )
    venta_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return venta_id


def obtener_ventas():
    """Obtiene todas las ventas registradas junto con el nombre del paciente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT v.*, p.nombre AS paciente_nombre, p.telefono AS paciente_telefono
        FROM ventas v
        INNER JOIN pacientes p ON v.paciente_id = p.id
        ORDER BY v.fecha_venta DESC
        """
    )
    filas = cursor.fetchall()
    conn.close()
    return filas


def obtener_ventas_por_paciente(paciente_id):
    """Obtiene el historial de ventas de un paciente específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM ventas
        WHERE paciente_id = ?
        ORDER BY fecha_venta DESC
        """,
        (paciente_id,),
    )
    filas = cursor.fetchall()
    conn.close()
    return filas


def obtener_ventas_pendientes():
    """Obtiene las ventas con saldo pendiente o entrega en proceso."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT v.*, p.nombre AS paciente_nombre, p.telefono AS paciente_telefono
        FROM ventas v
        INNER JOIN pacientes p ON v.paciente_id = p.id
        WHERE v.saldo_pendiente > 0 OR v.estatus_entrega != 'Entregado'
        ORDER BY v.fecha_venta ASC
        """
    )
    filas = cursor.fetchall()
    conn.close()
    return filas


def actualizar_pago_y_entrega(
    venta_id, anticipo, saldo_pendiente, estatus_pago, estatus_entrega
):
    """Actualiza el abono, saldo restante y estatus de pago/entrega de una venta."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE ventas
        SET anticipo = ?, saldo_pendiente = ?, estatus_pago = ?, estatus_entrega = ?
        WHERE id = ?
        """,
        (anticipo, saldo_pendiente, estatus_pago, estatus_entrega, venta_id),
    )
    cambios = cursor.rowcount
    conn.commit()
    conn.close()
    return cambios > 0


def eliminar_venta(venta_id):
    """Elimina una venta por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
    cambios = cursor.rowcount
    conn.commit()
    conn.close()
    return cambios > 0


# =====================================================================
# GESTIÓN DE CIERRES DE RUTA (FINANZAS OPERATIVAS SIMPLES)
# =====================================================================

def crear_cierre_ruta(
    localidad_id,
    fecha,
    total_venta=0.0,
    gastos_viaticos=0.0,
    gastos_materiales=0.0,
    gastos_armazones=0.0,
    gastos_maquilas=0.0,
    gastos_accesorios=0.0,
):
    """Registra el cierre financiero simple de una ruta o fecha."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cierres_ruta (
            localidad_id, fecha, total_venta, gastos_viaticos,
            gastos_materiales, gastos_armazones, gastos_maquilas, gastos_accesorios
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            localidad_id,
            fecha,
            total_venta,
            gastos_viaticos,
            gastos_materiales,
            gastos_armazones,
            gastos_maquilas,
            gastos_accesorios,
        ),
    )
    cierre_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return cierre_id


def obtener_cierres_ruta():
    """Obtiene todos los cierres de ruta ordenados por fecha más reciente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT c.*, l.nombre AS localidad_nombre
        FROM cierres_ruta c
        LEFT JOIN localidades l ON c.localidad_id = l.id
        ORDER BY c.fecha DESC, c.id DESC
        """
    )
    filas = cursor.fetchall()
    conn.close()
    return filas