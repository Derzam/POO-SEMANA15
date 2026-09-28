"""Panel de gestión con catálogo CRUD y consulta de usuarios."""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from ui.venta_view import VentaView


class MainView(tk.Frame):
    """Panel principal que presenta productos y usuarios del restaurante."""

    def __init__(
        self, master, restaurante_servicio, venta_servicio, al_cerrar_sesion
    ) -> None:
        super().__init__(master, padx=22, pady=22)
        self._restaurante_servicio = restaurante_servicio
        self._venta_servicio = venta_servicio
        self._al_cerrar_sesion = al_cerrar_sesion
        self._codigo_original = None
        self._campos = {}
        self._logo_image = None
        self._construir_widgets()

    def _construir_widgets(self) -> None:
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", pady=(0, 14))

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "restaurante_logo.ppm"
        try:
            self._logo_image = tk.PhotoImage(file=str(ruta_logo)).subsample(5, 5)
            ttk.Label(encabezado, image=self._logo_image).pack(side="left", padx=(0, 10))
        except tk.TclError:
            # Muestra el título si el recurso gráfico no puede cargarse.
            ttk.Label(encabezado, text="🍽", font=("Segoe UI Emoji", 20)).pack(side="left", padx=(0, 10))
        ttk.Label(
            encabezado, text="Gestión del restaurante", font=("Segoe UI", 17, "bold")
        ).pack(side="left")

        self._label_bienvenida = ttk.Label(encabezado, text="Bienvenido")
        self._label_bienvenida.pack(side="left", padx=(18, 0))

        ttk.Button(
            encabezado, text="Cerrar sesión", command=self._al_cerrar_sesion
        ).pack(side="right")

        resumen = ttk.Frame(self)
        resumen.pack(fill="x", pady=(0, 14))
        self._label_resumen = ttk.Label(resumen, text="")
        self._label_resumen.pack(side="left")

        self._pestañas = ttk.Notebook(self)
        self._pestañas.pack(fill="both", expand=True)
        self._pestañas.bind("<<NotebookTabChanged>>", self._al_cambiar_pestaña)
        self._construir_pestaña_productos()
        self._construir_pestaña_usuarios()
        self._construir_pestaña_ventas()

    def _construir_pestaña_productos(self) -> None:
        pestaña = ttk.Frame(self._pestañas, padding=12)
        pestaña.columnconfigure(0, weight=1)
        pestaña.rowconfigure(1, weight=1)
        self._pestañas.add(pestaña, text="Productos")

        formulario = ttk.LabelFrame(pestaña, text="Datos del producto", padding=12)
        formulario.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        for columna in range(5):
            formulario.columnconfigure(columna, weight=1)

        etiquetas = (
            ("Código", "codigo"),
            ("Nombre", "nombre"),
            ("Categoría", "categoria"),
            ("Precio", "precio"),
            ("Stock", "stock"),
        )
        anchos = {"codigo": 14, "nombre": 24, "categoria": 19, "precio": 12, "stock": 10}
        for columna, (titulo, clave) in enumerate(etiquetas):
            ttk.Label(formulario, text=titulo).grid(
                row=0, column=columna, sticky="w", padx=5, pady=(0, 4)
            )
            entrada = ttk.Entry(formulario, width=anchos[clave])
            entrada.grid(row=1, column=columna, sticky="ew", padx=5, pady=(0, 10))
            self._campos[clave] = entrada

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, sticky="w", padx=3)
        ttk.Button(acciones, text="Buscar", command=self._buscar_producto).pack(
            side="left", padx=(0, 7)
        )
        ttk.Button(acciones, text="Registrar", command=self._registrar_producto).pack(
            side="left", padx=7
        )
        ttk.Button(acciones, text="Actualizar", command=self._actualizar_producto).pack(
            side="left", padx=7
        )
        ttk.Button(acciones, text="Eliminar", command=self._eliminar_producto).pack(
            side="left", padx=7
        )
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_formulario).pack(
            side="left", padx=7
        )

        tabla_marco = ttk.LabelFrame(pestaña, text="Productos registrados", padding=8)
        tabla_marco.grid(row=1, column=0, sticky="nsew")
        tabla_marco.columnconfigure(0, weight=1)
        tabla_marco.rowconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock", "disponible")
        self._tabla_productos = ttk.Treeview(
            tabla_marco, columns=columnas, show="headings", selectmode="browse"
        )
        encabezados = {
            "codigo": ("Código", 90),
            "nombre": ("Nombre", 220),
            "categoria": ("Categoría", 150),
            "precio": ("Precio", 100),
            "stock": ("Stock", 80),
            "disponible": ("Disponibilidad", 125),
        }
        for clave, (titulo, ancho) in encabezados.items():
            self._tabla_productos.heading(clave, text=titulo)
            self._tabla_productos.column(clave, anchor="center", width=ancho)
        scrollbar = ttk.Scrollbar(
            tabla_marco, orient="vertical", command=self._tabla_productos.yview
        )
        self._tabla_productos.configure(yscrollcommand=scrollbar.set)
        self._tabla_productos.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._tabla_productos.bind("<<TreeviewSelect>>", self._al_seleccionar_producto)

        self._estado_productos = ttk.Label(pestaña, text="Selecciona una fila o busca por código.")
        self._estado_productos.grid(row=2, column=0, sticky="w", pady=(8, 0))

    def _construir_pestaña_usuarios(self) -> None:
        pestaña = ttk.Frame(self._pestañas, padding=12)
        pestaña.columnconfigure(0, weight=1)
        pestaña.rowconfigure(0, weight=1)
        self._pestañas.add(pestaña, text="Usuarios")

        tabla_marco = ttk.LabelFrame(pestaña, text="Usuarios registrados", padding=8)
        tabla_marco.grid(row=0, column=0, sticky="nsew")
        tabla_marco.columnconfigure(0, weight=1)
        tabla_marco.rowconfigure(0, weight=1)

        columnas = ("identificacion", "nombre", "usuario")
        self._tabla_usuarios = ttk.Treeview(
            tabla_marco, columns=columnas, show="headings", selectmode="browse"
        )
        encabezados = {
            "identificacion": ("Identificación", 160),
            "nombre": ("Nombre", 260),
            "usuario": ("Usuario", 180),
        }
        for clave, (titulo, ancho) in encabezados.items():
            self._tabla_usuarios.heading(clave, text=titulo)
            self._tabla_usuarios.column(clave, anchor="center", width=ancho)
        scrollbar = ttk.Scrollbar(
            tabla_marco, orient="vertical", command=self._tabla_usuarios.yview
        )
        self._tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self._tabla_usuarios.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _construir_pestaña_ventas(self) -> None:
        pestaña = ttk.Frame(self._pestañas, padding=18)
        self._pestañas.add(pestaña, text="Ventas")
        self._vista_ventas = VentaView(
            pestaña,
            venta_servicio=self._venta_servicio,
            restaurante_servicio=self._restaurante_servicio,
            al_registrar_venta=self._al_registrar_venta,
        )
        self._vista_ventas.pack(fill="both", expand=True)

    def actualizar(self, usuario_autenticado) -> None:
        self._label_bienvenida.config(text=f"Bienvenido, {usuario_autenticado.nombre}")
        self._refrescar_tabla_productos()
        self._refrescar_tabla_usuarios()
        self._actualizar_resumen()
        self._vista_ventas.actualizar(usuario_autenticado)

    def _al_registrar_venta(self, _venta, _producto) -> None:
        """Refresca el catálogo y el resumen luego de completar una venta."""
        self._refrescar_tabla_productos()
        self._actualizar_resumen()

    def _al_cambiar_pestaña(self, _evento=None) -> None:
        """Refresca las opciones al volver a Ventas después de editar productos."""
        if self._pestañas.select() == str(self._vista_ventas.master):
            self._vista_ventas.actualizar()

    def _leer_formulario(self) -> dict:
        return {clave: entrada.get() for clave, entrada in self._campos.items()}

    def _buscar_producto(self) -> None:
        codigo = self._campos["codigo"].get()
        producto = self._restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado("No se encontró un producto con ese código.", error=True)
            return
        self._cargar_formulario(producto)
        self._mostrar_estado(f"Producto {producto.codigo} cargado para consulta o edición.")

    def _al_seleccionar_producto(self, _evento=None) -> None:
        seleccion = self._tabla_productos.selection()
        if not seleccion:
            return
        valores = self._tabla_productos.item(seleccion[0], "values")
        producto = self._restaurante_servicio.buscar_producto(str(valores[0]))
        if producto is not None:
            self._cargar_formulario(producto)

    def _cargar_formulario(self, producto) -> None:
        for clave, entrada in self._campos.items():
            entrada.delete(0, tk.END)
            entrada.insert(0, str(getattr(producto, clave)))
        self._codigo_original = producto.codigo

    def _registrar_producto(self) -> None:
        try:
            producto = self._restaurante_servicio.registrar_producto(
                **self._leer_formulario()
            )
        except (ValueError, OSError) as error:
            self._mostrar_estado(str(error), error=True)
            return
        self._refrescar_tabla_productos()
        self._actualizar_resumen()
        self._seleccionar_fila(producto.codigo)
        self._mostrar_estado(f"Producto {producto.codigo} registrado y guardado.")

    def _actualizar_producto(self) -> None:
        if self._codigo_original is None:
            self._mostrar_estado("Busca o selecciona un producto antes de actualizar.", error=True)
            return
        try:
            producto = self._restaurante_servicio.actualizar_producto(
                self._codigo_original, **self._leer_formulario()
            )
        except (ValueError, OSError) as error:
            self._mostrar_estado(str(error), error=True)
            return
        self._refrescar_tabla_productos()
        self._actualizar_resumen()
        self._seleccionar_fila(producto.codigo)
        self._mostrar_estado(f"Producto {producto.codigo} actualizado y guardado.")

    def _eliminar_producto(self) -> None:
        if self._codigo_original is None:
            self._mostrar_estado("Busca o selecciona un producto antes de eliminar.", error=True)
            return
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el producto {self._codigo_original}?",
            parent=self,
        ):
            return
        codigo = self._codigo_original
        try:
            self._restaurante_servicio.eliminar_producto(codigo)
        except (ValueError, OSError) as error:
            self._mostrar_estado(str(error), error=True)
            return
        self._refrescar_tabla_productos()
        self._actualizar_resumen()
        self._limpiar_formulario()
        self._mostrar_estado(f"Producto {codigo} eliminado.")

    def _limpiar_formulario(self) -> None:
        for entrada in self._campos.values():
            entrada.delete(0, tk.END)
        self._codigo_original = None
        seleccion = self._tabla_productos.selection()
        if seleccion:
            self._tabla_productos.selection_remove(*seleccion)
        self._mostrar_estado("Formulario listo para un producto nuevo.")
        self._campos["codigo"].focus_set()

    def _refrescar_tabla_productos(self) -> None:
        self._tabla_productos.delete(*self._tabla_productos.get_children())
        for indice, producto in enumerate(self._restaurante_servicio.listar_productos()):
            self._tabla_productos.insert(
                "",
                tk.END,
                iid=f"producto-{indice}",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"$ {producto.precio:.2f}",
                    producto.stock,
                    "Disponible" if producto.disponible else "Agotado",
                ),
            )

    def _seleccionar_fila(self, codigo: str) -> None:
        for fila in self._tabla_productos.get_children():
            valores = self._tabla_productos.item(fila, "values")
            if str(valores[0]).casefold() == codigo.casefold():
                self._tabla_productos.selection_set(fila)
                self._tabla_productos.focus(fila)
                self._tabla_productos.see(fila)
                break

    def _refrescar_tabla_usuarios(self) -> None:
        self._tabla_usuarios.delete(*self._tabla_usuarios.get_children())
        for indice, usuario in enumerate(self._restaurante_servicio.listar_usuarios()):
            self._tabla_usuarios.insert(
                "",
                tk.END,
                iid=f"usuario-{indice}",
                values=(usuario.identificacion, usuario.nombre, usuario.usuario),
            )

    def _actualizar_resumen(self) -> None:
        self._label_resumen.config(
            text=(
                f"{self._restaurante_servicio.total_productos()} productos"
                f"   ·   {self._restaurante_servicio.total_usuarios()} usuarios"
            )
        )

    def _mostrar_estado(self, mensaje: str, error: bool = False) -> None:
        self._estado_productos.config(
            text=mensaje,
            foreground="#a12622" if error else "#25643b",
        )
