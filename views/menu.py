"""Módulo para desplegar los menús de navegación en la terminal."""

import sys
from controllers import (
    registrar_localidad,
    listar_localidades,
    registrar_paciente,
    listar_pacientes,
    buscar_pacientes_por_nombre
)


def mostrar_menu_principal():
    """Muestra las opciones generales del sistema."""
    print("\n" + "=" * 45)
    print("      SISTEMA DE GESTIÓN - ÓPTICA MIDU      ")
    print("=" * 45)
    print("1. Menú de Localidades / Campañas")
    print("2. Menú de Pacientes y Expedientes")
    print("0. Salir")
    print("=" * 45)


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
            nombre = input("Nombre completo del paciente: ").strip()
            telefono = input("Teléfono: ").strip()
            edad_str = input("Edad: ").strip()
            edad = int(edad_str) if edad_str.isdigit() else None

            print("\n--- DATOS DE GRADUACIÓN ---")
            od = input("Graduación Ojo Derecho (OD): ").strip()
            oi = input("Graduación Ojo Izquierdo (OI): ").strip()
            add = input("Presbicia / Adición (ADD): ").strip()
            obs = input("Observaciones: ").strip()

            if nombre:
                pac_id = registrar_paciente(
                    nombre=nombre,
                    telefono=telefono,
                    edad=edad,
                    graduacion_od=od,
                    graduacion_oi=oi,
                    presbicia=add,
                    observaciones=obs
                )
                print(f"✅ Paciente registrado con éxito (ID: {pac_id}).")
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


def iniciar_aplicacion():
    """Bucle principal de la interfaz."""
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_localidades()
        elif opcion == "2":
            menu_pacientes()
        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema de Óptica Midu! Hasta luego.")
            sys.exit()
        else:
            print("Opción no válida. Intenta de nuevo.")