"""Punto de entrada principal para la aplicación Óptica Midu."""

from database.connection import init_db
from views.menu import iniciar_aplicacion

if __name__ == "__main__":
    # Crea la base de datos y sus tablas si aún no existen
    init_db()
    # Arranca el menú interactivo en la consola
    iniciar_aplicacion()