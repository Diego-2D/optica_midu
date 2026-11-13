"""Componentes y vistas interactivas para la TUI de Servicios Ópticos MIDU."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Input, Label, Select, Static

from controllers import (
    listar_cierres_ruta,
    listar_localidades,
    listar_pacientes,
    listar_pendientes_cobranza,
    registrar_abono_o_entrega,
    registrar_cierre_ruta,
    registrar_localidad,
    registrar_paciente,
    registrar_venta,
)


class VistaFinanzasSimple(VerticalScroll):
    """Panel de resumen financiero simple y captura de cierre de ruta."""

    def compose(self) -> ComposeResult:
        cierres = listar_cierres_ruta()
        ultimo = cierres[0] if cierres else None

        ruta_txt = (
            f"{ultimo.localidad_nombre or 'General'} ({ultimo.fecha})"
            if ultimo
            else "Sin cierres registrados"
        )
        venta = ultimo.total_venta if ultimo else 0.0
        g_viat = ultimo.gastos_viaticos if ultimo else 0.0
        g_mat = ultimo.gastos_materiales if ultimo else 0.0
        g_arm = ultimo.gastos_armazones if ultimo else 0.0
        g_maq = ultimo.gastos_maquilas if ultimo else 0.0
        g_acc = ultimo.gastos_accesorios if ultimo else 0.0
        tot_gastos = ultimo.total_gastos if ultimo else 0.0
        utilidad = ultimo.utilidad_neta if ultimo else 0.0

        yield Label(f"ÚLTIMO CIERRE REGISTRADO: {ruta_txt}", classes="kpi_header")
        yield Label(f"• TOTAL DE VENTA ....................................... ${venta:,.2f} MXN", classes="kpi_row")
        yield Label(f"• GASTOS VIÁTICOS ...................................... ${g_viat:,.2f} MXN", classes="kpi_row")
        yield Label(f"• GASTOS MATERIALES .................................... ${g_mat:,.2f} MXN", classes="kpi_row")
        yield Label(f"• GASTOS ARMAZONES ..................................... ${g_arm:,.2f} MXN", classes="kpi_row")
        yield Label(f"• GASTOS MAQUILAS ...................................... ${g_maq:,.2f} MXN", classes="kpi_row")
        yield Label(f"• GASTOS ACCESORIOS .................................... ${g_acc:,.2f} MXN", classes="kpi_row")
        yield Static(classes="divider")
        yield Label(f"[-] TOTAL GASTOS OPERATIVOS ............................ ${tot_gastos:,.2f} MXN", classes="kpi_row")
        yield Label(f"[=] UTILIDAD NETA DE RUTA .............................. ${utilidad:,.2f} MXN", classes="kpi_profit")
        yield Static(classes="divider")

        yield Label("REGISTRAR NUEVO CIERRE DE RUTA / JORNADA:", classes="kpi_section")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="ID Localidad (opcional)", id="fin_loc_id", classes="input_half")
            yield Input(placeholder="Fecha YYYY-MM-DD (vacío = hoy)", id="fin_fecha", classes="input_half")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="Total Venta ($)", id="fin_venta", classes="input_half")
            yield Input(placeholder="Gastos Viáticos ($)", id="fin_viaticos", classes="input_half")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="Gastos Materiales ($)", id="fin_materiales", classes="input_half")
            yield Input(placeholder="Gastos Armazones ($)", id="fin_armazones", classes="input_half")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="Gastos Maquilas ($)", id="fin_maquilas", classes="input_half")
            yield Input(placeholder="Gastos Accesorios ($)", id="fin_accesorios", classes="input_half")

        yield Button("Guardar Cierre Financiero", id="btn_guardar_cierre", variant="success")
        yield Label("", id="fin_msg", classes="status_msg")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "btn_guardar_cierre":
            return

        def _num(widget_id: str) -> float:
            val = self.query_one(f"#{widget_id}", Input).value.strip()
            try:
                return float(val) if val else 0.0
            except ValueError:
                return 0.0

        loc_val = self.query_one("#fin_loc_id", Input).value.strip()
        loc_id = int(loc_val) if loc_val.isdigit() else None
        fecha = self.query_one("#fin_fecha", Input).value.strip()

        registrar_cierre_ruta(
            localidad_id=loc_id,
            fecha=fecha,
            total_venta=_num("fin_venta"),
            gastos_viaticos=_num("fin_viaticos"),
            gastos_materiales=_num("fin_materiales"),
            gastos_armazones=_num("fin_armazones"),
            gastos_maquilas=_num("fin_maquilas"),
            gastos_accesorios=_num("fin_accesorios"),
        )
        self.app.cargar_vista("nav_reporte")


class VistaCampanas(VerticalScroll):
    """Panel para registrar y consultar localidades o campañas."""

    def compose(self) -> ComposeResult:
        yield Label("NUEVA LOCALIDAD / RUTA:", classes="kpi_section")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="Nombre (ej. Jiquilpan)", id="loc_nombre", classes="input_half")
            yield Input(placeholder="Punto de atención (ej. Plaza Principal)", id="loc_ubicacion", classes="input_half")
        yield Button("Registrar Campaña", id="btn_guardar_loc", variant="warning")
        yield Label("", id="loc_msg", classes="status_msg")
        yield Static(classes="divider")
        yield Label("CAMPAÑAS REGISTRADAS:", classes="kpi_section")
        yield DataTable(id="tabla_localidades")

    def on_mount(self) -> None:
        tabla = self.query_one("#tabla_localidades", DataTable)
        tabla.add_columns("ID", "Localidad", "Punto de Atención", "Estado")
        self._refrescar_tabla()

    def _refrescar_tabla(self) -> None:
        tabla = self.query_one("#tabla_localidades", DataTable)
        tabla.clear()
        for loc in listar_localidades():
            tabla.add_row(str(loc.id), loc.nombre, loc.ubicacion, loc.estado)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_guardar_loc":
            nombre = self.query_one("#loc_nombre", Input).value.strip()
            ubicacion = self.query_one("#loc_ubicacion", Input).value.strip()
            msg = self.query_one("#loc_msg", Label)
            if not nombre or not ubicacion:
                msg.update("❌ Nombre y punto de atención son obligatorios.")
                return
            loc_id = registrar_localidad(nombre, ubicacion)
            self.query_one("#loc_nombre", Input).value = ""
            self.query_one("#loc_ubicacion", Input).value = ""
            msg.update(f"✅ Campaña '{nombre}' registrada con ID: {loc_id}")
            self._refrescar_tabla()


class VistaPacientes(VerticalScroll):
    """Panel de captura clínica y comercial de pacientes en campo."""

    def compose(self) -> ComposeResult:
        yield Label("1. DATOS DEL PACIENTE Y GRADUACIÓN:", classes="kpi_section")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="Nombre completo *", id="pac_nombre", classes="input_half")
            yield Input(placeholder="Teléfono", id="pac_tel", classes="input_third")
            yield Input(placeholder="Edad", id="pac_edad", classes="input_sixth")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="ID Localidad", id="pac_loc_id", classes="input_quarter")
            yield Input(placeholder="OD (Ojo Derecho)", id="pac_od", classes="input_quarter")
            yield Input(placeholder="OI (Ojo Izquierdo)", id="pac_oi", classes="input_quarter")
            yield Input(placeholder="ADD / Presbicia", id="pac_add", classes="input_quarter")
        yield Input(placeholder="Observaciones clínicas (opcional)", id="pac_obs")

        yield Label("2. ESPECIFICACIONES DEL LENTE Y VENTA (OPCIONAL):", classes="kpi_section")
        with Horizontal(classes="form_row"):
            yield Select(
                [
                    ("Monofocal", "Monofocal"),
                    ("Bifocal", "Bifocal"),
                    ("Invisible", "Invisible"),
                    ("Progresivo", "Progresivo"),
                ],
                prompt="Tipo de Lente",
                id="ven_tipo",
                classes="input_half",
            )
            yield Select(
                [
                    ("Blanco (Sin AR)", "Blanco (Sin AR)"),
                    ("Antirreflejante", "Antirreflejante"),
                    ("Blue", "Blue"),
                    ("Fotocromático", "Fotocromático"),
                    ("Foto AR", "Foto AR"),
                    ("Foto Blue", "Foto Blue"),
                ],
                prompt="Tratamiento",
                id="ven_tratamiento",
                classes="input_half",
            )

        with Horizontal(classes="form_row"):
            yield Select(
                [
                    ("Genérico", "Genérico"),
                    ("Easy Fit", "Easy Fit"),
                    ("Digital", "Digital"),
                    ("Otro", "Otro"),
                ],
                prompt="Diseño Progresivo",
                id="ven_diseno",
                classes="input_quarter",
                disabled=True,
            )
            yield Input(
                placeholder="Especificar cuál...",
                id="ven_diseno_otro",
                classes="input_quarter",
                disabled=True,
            )
            yield Select(
                [
                    ("Propio / Ninguno", "Propio / Ninguno"),
                    ("Económico", "Económico"),
                    ("Acetato", "Acetato"),
                    ("Línea", "Línea"),
                    ("Marca", "Marca"),
                ],
                prompt="Calidad Armazón",
                id="ven_armazon",
                classes="input_half",
            )

        with Horizontal(classes="form_row"):
            yield Input(placeholder="Total Trabajo ($ MXN)", id="ven_total", classes="input_half")
            yield Input(placeholder="Anticipo Recibido ($ MXN)", id="ven_anticipo", classes="input_half")

        yield Button("Guardar Paciente y Orden", id="btn_guardar_paciente", variant="success")
        yield Label("", id="pac_msg", classes="status_msg")
        yield Static(classes="divider")
        yield Label("ÚLTIMOS PACIENTES REGISTRADOS:", classes="kpi_section")
        yield DataTable(id="tabla_pacientes")

    def on_mount(self) -> None:
        tabla = self.query_one("#tabla_pacientes", DataTable)
        tabla.add_columns("ID", "Paciente", "Teléfono", "Graduación")
        self._refrescar_tabla()

    def _refrescar_tabla(self) -> None:
        tabla = self.query_one("#tabla_pacientes", DataTable)
        tabla.clear()
        for pac in listar_pacientes()[:15]:
            tabla.add_row(str(pac.id), pac.nombre, pac.telefono or "-", pac.resumen_graduacion)

    def on_select_changed(self, event: Select.Changed) -> None:
        """Habilita el selector de diseño si es Progresivo, y el texto si elige Otro."""
        if event.select.id == "ven_tipo":
            sel_diseno = self.query_one("#ven_diseno", Select)
            inp_otro = self.query_one("#ven_diseno_otro", Input)
            if event.value == "Progresivo":
                sel_diseno.disabled = False
            else:
                sel_diseno.value = Select.BLANK
                sel_diseno.disabled = True
                inp_otro.value = ""
                inp_otro.disabled = True

        elif event.select.id == "ven_diseno":
            inp_otro = self.query_one("#ven_diseno_otro", Input)
            if event.value == "Otro":
                inp_otro.disabled = False
                inp_otro.focus()
            else:
                inp_otro.value = ""
                inp_otro.disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Cuando se presiona Progresivo"""
        if event.button.id != "btn_guardar_paciente":
            return

        msg = self.query_one("#pac_msg", Label)
        nombre = self.query_one("#pac_nombre", Input).value.strip()
        if not nombre:
            msg.update("❌ El nombre del paciente es obligatorio.")
            return

        tel = self.query_one("#pac_tel", Input).value.strip()
        edad_str = self.query_one("#pac_edad", Input).value.strip()
        loc_str = self.query_one("#pac_loc_id", Input).value.strip()
        od = self.query_one("#pac_od", Input).value.strip()
        oi = self.query_one("#pac_oi", Input).value.strip()
        add = self.query_one("#pac_add", Input).value.strip()
        obs = self.query_one("#pac_obs", Input).value.strip()

        pac_id = registrar_paciente(
            nombre=nombre,
            telefono=tel,
            edad=int(edad_str) if edad_str.isdigit() else None,
            graduacion_od=od,
            graduacion_oi=oi,
            presbicia=add,
            observaciones=obs,
            localidad_id=int(loc_str) if loc_str.isdigit() else None,
        )

        # Revisar si también se capturó importe o especificaciones de lente
        total_str = self.query_one("#ven_total", Input).value.strip()
        anticipo_str = self.query_one("#ven_anticipo", Input).value.strip()
        tipo_val = self.query_one("#ven_tipo", Select).value
        trat_val = self.query_one("#ven_tratamiento", Select).value
        dis_val = self.query_one("#ven_diseno", Select).value
        arm_val = self.query_one("#ven_armazon", Select).value

        tipo_lente = None if tipo_val == Select.BLANK else str(tipo_val)
        tratamiento = None if trat_val == Select.BLANK else str(trat_val)
        diseno = None if dis_val == Select.BLANK else str(dis_val)
        if diseno == "Otro":
            otro_txt = self.query_one("#ven_diseno_otro", Input).value.strip()
            diseno = f"Otro: {otro_txt}" if otro_txt else "Otro"
        armazon = None if arm_val == Select.BLANK else str(arm_val)

        if total_str or tipo_lente:
            try:
                total_num = float(total_str) if total_str else 0.0
                anticipo_num = float(anticipo_str) if anticipo_str else 0.0
                registrar_venta(
                    paciente_id=pac_id,
                    tipo_lente=tipo_lente,
                    tratamiento=tratamiento,
                    diseno_progresivo=diseno,
                    calidad_armazon=armazon,
                    total=total_num,
                    anticipo=anticipo_num,
                )
                msg.update(f"✅ Paciente #{pac_id} y orden de lente guardados.")
            except ValueError as err:
                msg.update(f"⚠️ Paciente guardado (#{pac_id}), pero error en venta: {err}")
        else:
            msg.update(f"✅ Paciente '{nombre}' registrado con ID #{pac_id}.")

        # Limpiar campos principales
        for inp_id in ("pac_nombre", "pac_tel", "pac_edad", "pac_od", "pac_oi", "pac_add", "pac_obs", "ven_total", "ven_anticipo"):
            self.query_one(f"#{inp_id}", Input).value = ""
        self._refrescar_tabla()


class VistaCobranza(VerticalScroll):
    """Panel para consultar saldos pendientes y registrar liquidaciones o entregas."""

    def compose(self) -> ComposeResult:
        yield Label("TRABAJOS PENDIENTES DE PAGO O ENTREGA:", classes="kpi_section")
        yield DataTable(id="tabla_cobranza")
        yield Static(classes="divider")
        yield Label("LIQUIDAR SALDO / MARCAR ENTREGA:", classes="kpi_section")
        with Horizontal(classes="form_row"):
            yield Input(placeholder="ID Venta", id="cob_venta_id", classes="input_third")
            yield Input(placeholder="Abono recibido ($)", id="cob_abono", classes="input_third")
            yield Select(
                [("En Proceso", "En Proceso"), ("Entregado", "Entregado")],
                value="Entregado",
                id="cob_entrega",
                classes="input_third",
            )
        yield Button("Actualizar Venta", id="btn_actualizar_cobro", variant="primary")
        yield Label("", id="cob_msg", classes="status_msg")

    def on_mount(self) -> None:
        tabla = self.query_one("#tabla_cobranza", DataTable)
        tabla.add_columns("Venta #", "Paciente", "Trabajo", "Total", "Saldo", "Entrega")
        self._refrescar_tabla()

    def _refrescar_tabla(self) -> None:
        tabla = self.query_one("#tabla_cobranza", DataTable)
        tabla.clear()
        for v in listar_pendientes_cobranza():
            tabla.add_row(
                str(v.id),
                v.paciente_nombre or "-",
                v.resumen_trabajo(),
                f"${v.total:,.2f}",
                f"${v.saldo_pendiente:,.2f}",
                v.estatus_entrega,
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "btn_actualizar_cobro":
            return

        msg = self.query_one("#cob_msg", Label)
        v_id_str = self.query_one("#cob_venta_id", Input).value.strip()
        abono_str = self.query_one("#cob_abono", Input).value.strip()
        entrega_val = str(self.query_one("#cob_entrega", Select).value)

        if not v_id_str.isdigit():
            msg.update("❌ Ingresa un ID de venta válido.")
            return

        venta_id = int(v_id_str)
        pendientes = listar_pendientes_cobranza()
        venta_obj = next((x for x in pendientes if x.id == venta_id), None)
        if not venta_obj:
            msg.update("❌ No se encontró esa venta en la lista de pendientes.")
            return

        try:
            abono_extra = float(abono_str) if abono_str else 0.0
            registrar_abono_o_entrega(
                venta_id=venta_id,
                total=venta_obj.total,
                nuevo_anticipo=venta_obj.anticipo + abono_extra,
                estatus_entrega=entrega_val,
            )
            self.query_one("#cob_venta_id", Input).value = ""
            self.query_one("#cob_abono", Input).value = ""
            msg.update(f"✅ Venta #{venta_id} actualizada ({entrega_val}).")
            self._refrescar_tabla()
        except ValueError as err:
            msg.update(f"❌ {err}")