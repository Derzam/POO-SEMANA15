# ============================================================
# modelos/usuario.py
# Clase Usuario — representa a los usuarios utilizados en la
# SIMULACIÓN de acceso a la aplicación (pantalla de login).
#
# Semana 13: a diferencia de la Usuario de la versión de
# consola (identificación, nombre, correo — un cliente del
# restaurante), esta Usuario incorpora credenciales ("usuario"
# y "contraseña") porque su propósito en esta etapa es distinto:
# permitir que RestauranteServicio valide el acceso antes de
# mostrar MainView.


from dataclasses import dataclass


@dataclass
class Usuario:
    """Representa un usuario registrado para la simulación de acceso."""

    identificacion: int  # Identificador único del usuario
    nombre: str  # Nombre completo del usuario
    usuario: str  # Nombre de usuario (login)
    contraseña: str  # Contraseña simulada (texto plano, solo con fines didácticos)

    def __post_init__(self) -> None:
        """Valida los datos del usuario apenas se construye el objeto,
        tanto si viene de datos.json como de una futura alta por consola."""
        try:
            self.identificacion = int(self.identificacion)
        except (TypeError, ValueError):
            raise ValueError("La identificación del usuario debe ser un número entero.")
        if self.identificacion <= 0:
            raise ValueError("La identificación del usuario debe ser un número positivo.")

        if not self.nombre or not str(self.nombre).strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self.nombre = str(self.nombre).strip()

        if not self.usuario or not str(self.usuario).strip():
            raise ValueError("El nombre de usuario (login) no puede estar vacío.")
        self.usuario = str(self.usuario).strip()

        if not isinstance(self.contraseña, str) or not self.contraseña:
            raise ValueError("La contraseña debe ser texto y no puede estar vacía.")

    def __str__(self) -> str:
        """Representación en texto del usuario (nunca incluye la contraseña)."""
        return f"[ID {self.identificacion}] {self.nombre} — usuario: {self.usuario}"

    # --------------------------------------------------------
    # Persistencia: conversión desde diccionario (JSON)
    # --------------------------------------------------------
    @classmethod
    def from_dict(cls, datos: dict) -> "Usuario":
        """Reconstruye un Usuario a partir de un diccionario leído del JSON.

        Si falta una clave obligatoria, Python lanza KeyError de forma
        natural; si un valor no es válido, __post_init__ propaga
        ValueError. En ambos casos ArchivoServicio decide cómo manejarlo.
        """
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            contraseña=datos["contraseña"],
        )

