import reflex as rx

# Paleta de colores moderna, pastel y limpia para PACTA
class Color:
    """Paleta de colores para la aplicación PACTA."""
    PRIMARY = "#A9D6E5"         # Azul pastel claro (cielo)
    PRIMARY_CONTENT = "#012A4A"  # Azul muy oscuro para texto sobre primario
    SECONDARY = "#E9ECEF"       # Gris claro para fondos secundarios/deshabilitados
    SECONDARY_CONTENT = "#495057" # Gris oscuro para texto sobre secundario
    ACCENT = "#468FAF"           # Azul acento (más saturado)
    ACCENT_LIGHT = "#89C2D9"     # Acento claro para hovers
    BACKGROUND = "#F8F9FA"       # Fondo principal (casi blanco)
    CONTENT = "#212529"          # Color de texto principal (gris oscuro)
    BORDER = "#DEE2E6"           # Color de borde sutil
    SUCCESS = "#A7C957"          # Verde pastel
    WARNING = "#F2E86D"          # Amarillo pastel
    ERROR = "#F26457"            # Rojo pastel
    WHITE = "#FFFFFF"

# Estilos base para la aplicación
BASE_STYLES = {
    rx.text: {
        "font_family": "Inter, sans-serif",
        "color": Color.CONTENT,
    },
    rx.heading: {
        "font_family": "Inter, sans-serif",
        "color": Color.PRIMARY_CONTENT,
    },
    rx.link: {
        "color": Color.ACCENT,
        "text_decoration": "none",
        "_hover": {
            "color": Color.ACCENT_LIGHT,
            "text_decoration": "underline",
        },
    },
    rx.button: {
        "border_radius": "0.375rem",
        "font_weight": "500",
        "transition": "background-color 0.2s ease-in-out, color 0.2s ease-in-out",
        "--cursor-button": "pointer",
        "background_color": Color.PRIMARY,
        "color": Color.PRIMARY_CONTENT,
        "_hover": {
            "background_color": Color.ACCENT_LIGHT,
        },
    },
    rx.input: {
        "border_radius": "0.375rem",
        "border": f"1px solid {Color.BORDER}",
    },
     rx.form: {
        "background_color": Color.WHITE,
        "padding": "2rem",
        "border_radius": "0.5rem",
        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    }
}

# Diccionario de estilos globales para ser importado
global_styles = {
    "font_family": "Inter, sans-serif",
    "background_color": Color.BACKGROUND,
    **BASE_STYLES,
}