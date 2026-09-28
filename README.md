Sistema de Gestión de Restaurante — Semana 15
Esta versión evoluciona la aplicación gráfica de la Semana 14. Conserva el login, la consulta de usuarios y el CRUD de productos, y añade el registro persistente de ventas.

Autor: Derly Zambrano

Estructura
restaurante_app/
├── assets/ (restaurante_logo.svg y restaurante_logo.ppm)
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   ├── restaurante_servicio.py
│   └── venta_servicio.py
├── ui/
│   ├── login_view.py
│   ├── main_view.py
│   └── venta_view.py
└── main.py
Componentes y operación
main.py prepara ArchivoServicio, RestauranteServicio y VentaServicio, y conserva una sola ventana principal. MainView organiza Productos, Usuarios y Ventas en pestañas Notebook. La vista de ventas agrupa el formulario con LabelFrame y Frame; utiliza Combobox para elegir usuario y producto disponible, Entry para indicar cantidad y Button con command para registrar la venta. El historial se consulta en Treeview con barras de desplazamiento. El logotipo Sazón Manaba se conserva en assets/restaurante_logo.svg y assets/restaurante_logo.ppm; la interfaz carga el PPM en el acceso y en la cabecera del panel.

VentaServicio valida la existencia del usuario y producto, que la cantidad sea un entero positivo y que no supere el stock. Después actualiza las existencias mediante RestauranteServicio y persiste la venta con ArchivoServicio. Venta registra fecha, usuario, producto, cantidad, precio unitario y total. El historial se guarda en datos/ventas.json; el nuevo stock, en datos/productos.json. La interfaz actualiza ambas vistas tras una venta correcta. No se implementan pagos, facturación ni descuentos.

Ejecución
Requisitos: Python 3.7 o posterior con Tkinter instalado. Desde esta carpeta:

python main.py
Credenciales de prueba en datos/usuarios.json:

Usuario	Contraseña
derly	admin123
prueba	1234
