-- TABLA DE LOCALIDADES (Logística, sedes y fechas)
CREATE TABLE IF NOT EXISTS localidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    presupuesto REAL DEFAULT 0.0,
    estado TEXT DEFAULT 'Planificada'
);

-- TABLA DE PACIENTES (Registro clínico y graduación)
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    localidad_id INTEGER,
    nombre TEXT NOT NULL,
    telefono TEXT,
    edad INTEGER,
    graduacion_od TEXT,
    graduacion_oi TEXT,
    presbicia TEXT,
    observaciones TEXT,
    FOREIGN KEY (localidad_id) REFERENCES localidades (id)
);

-- TABLA DE VENTAS Y COBRANZA (Control financiero)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    total REAL NOT NULL,
    anticipo REAL DEFAULT 0.0,
    saldo_pendiente REAL NOT NULL,
    estatus_pago TEXT DEFAULT 'Pendiente',
    estatus_entrega TEXT DEFAULT 'En Proceso',
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
);