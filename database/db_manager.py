from connection import get_connection


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

def obtener_pacientes_por_localidad(localidad_id):
    """Devuelve todos los pacientes atendidos en una localidad específica."""
    sql = "SELECT * FROM pacientes WHERE localidad_id = ? ORDER BY nombre ASC"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (localidad_id,))
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

# ==========================================
# VERIFICACIÓN DEL MODULO
# ==========================================

if __name__ == "__main__":
    print("Módulo db_manager.py cargado correctamente. Listo para recibir operaciones.")
    
"""
# ==========================================
# PRUEBA RÁPIDA DE LAS FUNCIONES CRUD
# ==========================================

    # 1. Creamos una localidad de prueba
    id_loc = crear_localidad("San Gabriel", "Plaza Principal", "2026-11-01", "2026-11-05", 5000.0)
    print(f"Localidad creada con ID: {id_loc}")
    
    # 2. Registramos un paciente en esa localidad
    id_pac = crear_paciente(
        localidad_id=id_loc,
        nombre="Juan Pérez",
        telefono="3312345678",
        edad=45,
        graduacion_od="+0.50",
        graduacion_oi="+0.75",
        presvicia="+1.50",
        observaciones="Lectura de cerca"
    )
    print(f"Paciente creado con ID: {id_pac}")
    
    # 3. Consultamos los datos ingresados
    pacientes = obtener_pacientes_por_localidad(id_loc)
    print(f"\nPacientes encontrados en la localidad {id_loc}:")
    for p in pacientes:
        print(f"- [{p['id']}] {p['nombre']} | OD: {p['graduacion_od']} | OI: {p['graduacion_oi']} | ADD: {p['presvicia']} | NOTA: {p['observaciones']}")
        """