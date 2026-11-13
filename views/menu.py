"""Módulo para desplegar los menús de navegación en la terminal (CLI)."""

import sys
from controllers import (
    registrar_localidad,
    listar_localidades,
    registrar_paciente,
    listar_pacientes,
    buscar_pacientes_por_nombre,
    registrar_venta,
    listar_ventas,
    listar_pendientes_cobranza,
    registrar_abono_o_entrega,
    registrar_cierre_ruta,
    listar_cierres_ruta,
)


def _leer_float(mensaje, default=0.0):
    """Auxiliar para leer montos numéricos sin romper el programa si se deja vacío."""
    valor = input(mensaje).strip()
    if not valor:
        return default
    try:
        return float(valor)
    except ValueError:
        print("⚠️ Valor numérico no válido, se asignará 0.0")
        return default


def _seleccionar_opcion(titulo, opciones):
    """Muestra un mini-selector numerado para captura rápida en campo."""
    print(f"\n{titulo}:")
    for idx, opcion in enumerate(opciones, start=1):
        print(f"  {idx}. {opcion}")
    eleccion = input("Elige número (o escribe texto personalizado): ").strip()
    if eleccion.isdigit():
        indice = int(eleccion) - 1
        if 0 <= indice < len(opciones):
            return opciones[indice]
    return eleccion if eleccion else None


def mostrar_menu_principal():
    """Muestra las opciones generales del sistema."""
    print("\n" + "=" * 50)
    print("   SERVICIOS ÓPTICOS MIDU - SISTEMA DE GESTIÓN   ")
    print("=" * 50)
    print("1. Localidades / Campañas")
    print("2. Pacientes y Expedientes Clínicos")
    print("3. Ventas, Lentes y Cobranza")
    print("4. Cierre Financiero de Ruta (Simple)")
    print("0. Salir")
    print("=" * 50)


def menu_localidades():
    """Despliega las opciones para gestionar localidades."""
    while True:
        print("\n--- GESTIÓN DE LOCALIDADES ---")
        print("1. Registrar nueva localidad")
        print("2. Listar todas las localidades")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre de la localidad/pueblo: ").strip()
            ubicacion = input("Ubicación/Punto de atención: ").strip()
            if nombre and ubicacion:
                loc_id = registrar_localidad(nombre, ubicacion)
                print(f"✅ Localidad registrada con éxito (ID: {loc_id}).")
            else:
                print("❌ El nombre y la ubicación son obligatorios.")
        elif opcion == "2":
            localidades = listar_localidades()
            if not localidades:
                print("No hay localidades registradas.")
            else:
                print("\n--- LISTA DE LOCALIDADES ---")
                for loc in localidades:
                    print(f"[{loc.id}] {loc.nombre} - {loc.ubicacion} ({loc.estado})")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def _capturar_datos_venta(paciente_id):
    """Flujo guiado para capturar el lente, armazón, precio y anticipo."""
    print("\n--- DATOS DEL LENTE Y VENTA ---")
    tipo_lente = _seleccionar_opcion(
        "Tipo de Lente", ["Monofocal", "Bifocal", "Invisible", "Progresivo"]
    )
    tratamiento = _seleccionar_opcion(
        "Tratamiento / Recubrimiento",
        ["Blanco (Sin AR)", "Antirreflejante", "Blue", "Fotocromático", "Foto AR", "Foto Blue"],
    )

    diseno_progresivo = None
    if tipo_lente and tipo_lente.lower() == "progresivo":
        diseno_progresivo = _seleccionar_opcion(
            "Diseño de Progresivo", ["Genérico", "Easy Fit", "Digital", "Marca"]
        )

    calidad_armazon = _seleccionar_opcion(
        "Calidad de Armazón", ["Propio / Ninguno", "Económico", "Acetato", "Línea", "Marca"]
    )

    total = _leer_float("Precio total del trabajo ($ MXN): ")
    anticipo = _leer_float("Anticipo recibido ($ MXN) [Enter para 0]: ", default=0.0)

    try:
        venta_id = registrar_venta(
            paciente_id=paciente_id,
            tipo_lente=tipo_lente,
            tratamiento=tratamiento,
            diseno_progresivo=diseno_progresivo,
            calidad_armazon=calidad_armazon,
            total=total,
            anticipo=anticipo,
        )
        saldo = total - anticipo
        print(f"✅ Venta registrada (ID: {venta_id}) | Saldo pendiente: ${saldo:,.2f} MXN")
    except ValueError as err:
        print(f"❌ Error al registrar venta: {err}")


def menu_pacientes():
    """Despliega las opciones para gestionar pacientes."""
    while True:
        print("\n--- GESTIÓN DE PACIENTES ---")
        print("1. Registrar nuevo paciente")
        print("2. Ver padrón general de pacientes")
        print("3. Buscar paciente por nombre")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            loc_str = input("ID de Localidad (opcional, Enter para omitir): ").strip()
            localidad_id = int(loc_str) if loc_str.isdigit() else None

            nombre = input("Nombre completo del paciente: ").strip()
            telefono = input("Teléfono: ").strip()
            edad_str = input("Edad: ").strip()
            edad = int(edad_str) if edad_str.isdigit() else None

            print("\n--- DATOS DE GRADUACIÓN ---")
            od = input("Graduación Ojo Derecho (OD): ").strip()
            oi = input("Graduación Ojo Izquierdo (OI): ").strip()
            add = input("Presbicia / Adición (ADD): ").strip()
            obs = input("Observaciones clínicas: ").strip()

            if nombre:
                pac_id = registrar_paciente(
                    nombre=nombre,
                    telefono=telefono,
                    edad=edad,
                    graduacion_od=od,
                    graduacion_oi=oi,
                    presbicia=add,
                    observaciones=obs,
                    localidad_id=localidad_id,
                )
                print(f"✅ Paciente registrado con éxito (ID: {pac_id}).")

                agregar_venta = input("¿Deseas registrar su lente/venta ahora? (s/n): ").strip().lower()
                if agregar_venta == "s":
                    _capturar_datos_venta(pac_id)
            else:
                print("❌ El nombre del paciente es obligatorio.")
        elif opcion == "2":
            pacientes = listar_pacientes()
            if not pacientes:
                print("No hay pacientes registrados.")
            else:
                print("\n--- PADRÓN GENERAL DE PACIENTES ---")
                for pac in pacientes:
                    print(f"[{pac.id}] {pac.nombre} | Tel: {pac.telefono} | {pac.resumen_graduacion()}")
        elif opcion == "3":
            busqueda = input("Ingresa el nombre o apellido a buscar: ").strip()
            resultados = buscar_pacientes_por_nombre(busqueda)
            if not resultados:
                print("No se encontraron coincidencias.")
            else:
                print(f"\n--- RESULTADOS DE BÚSQUEDA ('{busqueda}') ---")
                for pac in resultados:
                    print(f"[{pac.id}] {pac.nombre} | {pac.resumen_graduacion()}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def menu_ventas():
    """Despliega las opciones para ventas, entregas y cobranza."""
    while True:
        print("\n--- VENTAS, LENTES Y COBRANZA ---")
        print("1. Registrar nueva venta a paciente existente")
        print("2. Ver todas las ventas")
        print("3. Ver pendientes de pago o entrega")
        print("4. Actualizar abono / marcar como entregado")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            pac_str = input("ID del Paciente: ").strip()
            if pac_str.isdigit():
                _capturar_datos_venta(int(pac_str))
            else:
                print("❌ Ingresa un ID numérico válido.")
        elif opcion == "2":
            ventas = listar_ventas()
            if not ventas:
                print("No hay ventas registradas.")
            else:
                print("\n--- HISTORIAL DE VENTAS ---")
                for v in ventas:
                    print(
                        f"[Venta #{v.id}] {v.paciente_nombre} | {v.resumen_trabajo()} | "
                        f"Total: ${v.total:,.2f} | Saldo: ${v.saldo_pendiente:,.2f} ({v.estatus_pago} / {v.estatus_entrega})"
                    )
        elif opcion == "3":
            pendientes = listar_pendientes_cobranza()
            if not pendientes:
                print("✅ No hay saldos ni entregas pendientes.")
            else:
                print("\n--- PENDIENTES DE COBRANZA / ENTREGA ---")
                for v in pendientes:
                    print(
                        f"[Venta #{v.id}] {v.paciente_nombre} (Tel: {v.paciente_telefono}) | "
                        f"Saldo: ${v.saldo_pendiente:,.2f} | Entrega: {v.estatus_entrega}"
                    )
        elif opcion == "4":
            pendientes = listar_pendientes_cobranza()
            if not pendientes:
                print("✅ No hay ventas pendientes por actualizar.")
                continue
            for v in pendientes:
                print(
                    f"[#{v.id}] {v.paciente_nombre} | Total: ${v.total:,.2f} | "
                    f"Abonado: ${v.anticipo:,.2f} | Resta: ${v.saldo_pendiente:,.2f} | {v.estatus_entrega}"
                )
            v_str = input("\nID de la Venta a actualizar: ").strip()
            if not v_str.isdigit():
                print("❌ ID no válido.")
                continue
            venta_id = int(v_str)
            venta_obj = next((x for x in pendientes if x.id == venta_id), None)
            if not venta_obj:
                print("❌ No se encontró esa venta en pendientes.")
                continue

            abono_extra = _leer_float(f"Nuevo abono recibido hoy (Resta ${venta_obj.saldo_pendiente:,.2f}): ")
            nuevo_anticipo = venta_obj.anticipo + abono_extra
            entregado = input("¿Se entrega el lente hoy? (s/n): ").strip().lower()
            nuevo_estatus_entrega = "Entregado" if entregado == "s" else venta_obj.estatus_entrega

            try:
                registrar_abono_o_entrega(
                    venta_id=venta_id,
                    total=venta_obj.total,
                    nuevo_anticipo=nuevo_anticipo,
                    estatus_entrega=nuevo_estatus_entrega,
                )
                print("✅ Venta actualizada correctamente.")
            except ValueError as err:
                print(f"❌ Error: {err}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def menu_finanzas_ruta():
    """Despliega el cierre operativo simple por fecha o localidad."""
    while True:
        print("\n--- CIERRE FINANCIERO DE RUTA (SIMPLE) ---")
        print("1. Registrar cierre de jornada / ruta")
        print("2. Consultar historial de cierres")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            loc_str = input("ID de Localidad (opcional, Enter para omitir): ").strip()
            localidad_id = int(loc_str) if loc_str.isdigit() else None
            fecha = input("Fecha (YYYY-MM-DD, Enter para hoy): ").strip()

            print("\n--- INGRESOS Y GASTOS DE LA RUTA ---")
            total_venta = _leer_float("Total de Venta ($ MXN): ")
            g_viaticos = _leer_float("Total Gastos Viáticos (gasolina/comidas): ")
            g_materiales = _leer_float("Total Gastos Materiales: ")
            g_armazones = _leer_float("Total Gastos Armazones: ")
            g_maquilas = _leer_float("Total Gastos Maquilas (laboratorio): ")
            g_accesorios = _leer_float("Total Gastos Accesorios (estuches/microfibras): ")

            cierre_id = registrar_cierre_ruta(
                localidad_id=localidad_id,
                fecha=fecha,
                total_venta=total_venta,
                gastos_viaticos=g_viaticos,
                gastos_materiales=g_materiales,
                gastos_armazones=g_armazones,
                gastos_maquilas=g_maquilas,
                gastos_accesorios=g_accesorios,
            )
            total_gastos = g_viaticos + g_materiales + g_armazones + g_maquilas + g_accesorios
            utilidad = total_venta - total_gastos
            print(
                f"✅ Cierre #{cierre_id} guardado | Gastos Totales: ${total_gastos:,.2f} | "
                f"Utilidad Neta: ${utilidad:,.2f} MXN"
            )
        elif opcion == "2":
            cierres = listar_cierres_ruta()
            if not cierres:
                print("No hay cierres financieros registrados.")
            else:
                print("\n--- HISTORIAL DE CIERRES DE RUTA ---")
                for c in cierres:
                    ruta_label = c.localidad_nombre if c.localidad_nombre else "General"
                    print(
                        f"[#{c.id}] Fecha: {c.fecha} ({ruta_label}) | "
                        f"Venta: ${c.total_venta:,.2f} | Gastos: ${c.total_gastos:,.2f} | "
                        f"Utilidad: ${c.utilidad_neta:,.2f} MXN"
                    )
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def iniciar_aplicacion():
    """Bucle principal de la interfaz CLI."""
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_localidades()
        elif opcion == "2":
            menu_pacientes()
        elif opcion == "3":
            menu_ventas()
        elif opcion == "4":
            menu_finanzas_ruta()
        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema de Servicios Ópticos MIDU! Hasta luego.")
            sys.exit()
        else:
            print("Opción no válida. Intenta de nuevo.")