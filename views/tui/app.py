"""Interfaz gráfica de terminal (TUI) para Servicios Ópticos MIDU usando Textual."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Static

from database.connection import init_db
from views.tui.vistas import (
    VistaCampanas,
    VistaCobranza,
    VistaFinanzasSimple,
    VistaPacientes,
)


class HeaderMidu(Horizontal):
    """Barra de título superior con contexto de campaña."""

    def compose(self) -> ComposeResult:
        yield Label("SERVICIOS ÓPTICOS MIDU - TUI SYSTEM v1.0", id="header_title")
        yield Label("[ Jalisco | Nov 2026 ]", id="header_context")


class SidebarMidu(Vertical):
    """Columna izquierda con el menú navegable y guía de controles."""

    def compose(self) -> ComposeResult:
        with Vertical(id="menu_box"):
            yield Label(" MENÚ PRINCIPAL ", classes="box_title_amber")
            yield ListView(
                ListItem(Label("1. Nueva Campaña / Ruta"), id="nav_campana"),
                ListItem(Label("2. Captura de Pacientes"), id="nav_pacientes"),
                ListItem(Label("3. Cierre Financiero Ruta"), id="nav_reporte"),
                ListItem(Label("4. Control de Cobranza"), id="nav_cobranza"),
                ListItem(Label("5. Salir"), id="nav_salir"),
                id="main_menu_list",
                initial_index=2,
            )

        with Vertical(id="controls_box"):
            yield Label(" CONTROLES ", classes="box_title_muted")
            yield Label("[↑/↓] Navegar Menú", classes="control_item")
            yield Label("[ENTER] Seleccionar", classes="control_item")
            yield Label("[TAB] Cambiar Campo", classes="control_item")
            yield Label("[ESC] Volver a Menú", classes="control_item")


class WorkspaceMidu(Vertical):
    """Panel derecho principal donde se renderizan las vistas dinámicas."""

    def compose(self) -> ComposeResult:
        with Vertical(id="workspace_box"):
            yield Label(" VISTA: CIERRE FINANCIERO DE RUTA ", id="workspace_title")
            yield Container(id="dynamic_content")


class StatusBarMidu(Static):
    """Barra de estado inferior conectada a SQLite."""

    def compose(self) -> ComposeResult:
        yield Label(
            "STATUS: Conectado a Base de Datos Local (SQLite) | Base: optica_midu.db",
            id="status_text",
        )


class OpticaMiduTUI(App):
    """Aplicación principal de terminal para Servicios Ópticos MIDU."""

    CSS = """
    Screen {
        background: #141c24;
        color: #e2e8f0;
        layout: vertical;
        border: heavy #38bdf8;
        padding: 0 1;
    }

    HeaderMidu {
        height: 3;
        border-bottom: double #334155;
        padding: 1 1 0 1;
        align: left middle;
    }

    #header_title {
        width: 1fr;
        color: #38bdf8;
        text-style: bold;
    }

    #header_context {
        width: auto;
        color: #94a3b8;
    }

    #body_container {
        height: 1fr;
        layout: horizontal;
        padding: 1 0;
    }

    SidebarMidu {
        width: 32;
        height: 1fr;
        margin-right: 2;
    }

    #menu_box {
        height: auto;
        border: round #f59e0b;
        padding: 1 1;
        margin-bottom: 1;
    }

    .box_title_amber {
        color: #f59e0b;
        text-style: bold;
        margin-bottom: 1;
    }

    ListView {
        height: auto;
        background: transparent;
    }

    ListItem {
        padding: 0 1;
        height: 2;
        color: #cbd5e1;
    }

    ListView:focus > ListItem.--highlight {
        background: #0f2942;
        color: #38bdf8;
        text-style: bold;
        border-left: outer #38bdf8;
    }

    #controls_box {
        height: auto;
        border: round #475569;
        padding: 1 2;
    }

    .box_title_muted {
        color: #94a3b8;
        text-style: bold;
        margin-bottom: 1;
    }

    .control_item {
        color: #94a3b8;
        height: 1;
    }

    WorkspaceMidu {
        width: 1fr;
        height: 1fr;
    }

    #workspace_box {
        height: 1fr;
        border: round #10b981;
        padding: 1 2;
    }

    #workspace_title {
        color: #10b981;
        text-style: bold;
        margin-bottom: 1;
    }

    #dynamic_content {
        height: 1fr;
    }

    .kpi_header {
        color: #f8fafc;
        text-style: bold;
        padding-bottom: 1;
        border-bottom: solid #475569;
        margin-bottom: 1;
    }

    .kpi_row {
        color: #e2e8f0;
        height: 1;
    }

    .kpi_profit {
        color: #10b981;
        text-style: bold;
        height: 1;
    }

    .kpi_section {
        color: #f59e0b;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    .divider {
        border-bottom: solid #475569;
        height: 1;
        margin: 1 0;
    }

    .form_row {
        height: auto;
        margin-bottom: 1;
    }

    .input_half {
        width: 1fr;
        margin-right: 1;
    }

    .input_third {
        width: 1fr;
        margin-right: 1;
    }

    .input_quarter {
        width: 1fr;
        margin-right: 1;
    }

    .input_sixth {
        width: 14;
    }

    .status_msg {
        color: #38bdf8;
        margin-top: 1;
    }

    DataTable {
        height: 12;
        margin-top: 1;
    }

    StatusBarMidu {
        height: 2;
        border-top: double #334155;
        padding: 0 1;
    }

    #status_text {
        color: #10b981;
    }
    """

    BINDINGS = [
        ("escape", "foco_menu", "Volver al menú"),
        ("q", "quit", "Salir"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderMidu()
        with Horizontal(id="body_container"):
            yield SidebarMidu()
            yield WorkspaceMidu()
        yield StatusBarMidu()

    def on_mount(self) -> None:
        init_db()
        self.query_one("#main_menu_list", ListView).focus()
        self.cargar_vista("nav_reporte")

    def action_foco_menu(self) -> None:
        self.query_one("#main_menu_list", ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.cargar_vista(event.item.id)

    def cargar_vista(self, item_id: str | None) -> None:
        titulo = self.query_one("#workspace_title", Label)
        contenedor = self.query_one("#dynamic_content", Container)
        contenedor.remove_children()

        if item_id == "nav_campana":
            titulo.update(" VISTA: GESTIÓN DE CAMPAÑAS / RUTAS ")
            contenedor.mount(VistaCampanas())
        elif item_id == "nav_pacientes":
            titulo.update(" VISTA: CAPTURA DE PACIENTES Y ÓRDENES ")
            contenedor.mount(VistaPacientes())
        elif item_id == "nav_reporte":
            titulo.update(" VISTA: CIERRE FINANCIERO DE RUTA (SIMPLE) ")
            contenedor.mount(VistaFinanzasSimple())
        elif item_id == "nav_cobranza":
            titulo.update(" VISTA: CONTROL DE COBRANZA Y ENTREGAS ")
            contenedor.mount(VistaCobranza())
        elif item_id == "nav_salir":
            self.exit()


if __name__ == "__main__":
    app = OpticaMiduTUI()
    app.run()