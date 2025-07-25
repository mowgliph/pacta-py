import reflex as rx

# Fuentes personalizadas
class Font:
    """Configuración de fuentes para la aplicación PACTA."""
    PRIMARY = "Poppins"
    SECONDARY = "Open Sans"
    DEFAULT = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

# Tamaños de fuente escalables
class FontSizes:
    """Tamaños de fuente predefinidos basados en una escala modular.
    
    Basado en un tamaño base de 1rem (16px por defecto) con una relación de 1.25.
    """
    XS = "0.75rem"      # 12px
    SM = "0.875rem"     # 14px
    BASE = "1rem"       # 16px
    LG = "1.25rem"      # 20px
    XL = "1.5rem"       # 24px
    XL2 = "1.875rem"    # 30px
    XL3 = "2.25rem"     # 36px
    XL4 = "3rem"        # 48px
    XL5 = "3.75rem"     # 60px
    XL6 = "4.5rem"      # 72px

# Configuración de estilos de texto
class TextStyles:
    """Estilos de texto predefinidos."""
    HEADING = {
        "font_family": Font.PRIMARY,
        "font_weight": "700",
        "line_height": "1.2",
        "font_size": FontSizes.XL4,
    }
    
    SUBHEADING = {
        "font_family": Font.PRIMARY,
        "font_weight": "600",
        "line_height": "1.3",
        "font_size": FontSizes.XL,  # 1.5rem / 24px
    }
    
    BODY = {
        "font_family": Font.SECONDARY,
        "font_weight": "400",
        "line_height": "1.6",
        "font_size": FontSizes.BASE,  # 1rem / 16px
    }
    
    SMALL = {
        "font_family": Font.SECONDARY,
        "font_size": FontSizes.SM,  # 0.875rem / 14px
        "line_height": "1.5",
    }

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
    "@import": [
        'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Open+Sans:wght@400;500;600&display=swap',
    ],
    "body": {
        "font_family": f"{Font.SECONDARY}, {Font.DEFAULT}",
        "color": Color.CONTENT,
        "line_height": "1.6",
        "font_size": FontSizes.BASE,  # 1rem / 16px
    },
    "h1": {
        "font_size": FontSizes.XL4,  # 3rem / 48px
        "font_weight": "700",
    },
    "h2": {
        "font_size": FontSizes.XL3,  # 2.25rem / 36px
        "font_weight": "700",
    },
    "h3": {
        "font_size": FontSizes.XL2,  # 1.875rem / 30px
        "font_weight": "600",
    },
    "h4": {
        "font_size": FontSizes.XL,  # 1.5rem / 24px
        "font_weight": "600",
    },
    "h5": {
        "font_size": FontSizes.LG,  # 1.25rem / 20px
        "font_weight": "600",
    },
    "h6": {
        "font_size": FontSizes.BASE,  # 1rem / 16px
        "font_weight": "600",
    },
    "h1, h2, h3, h4, h5, h6": {
        "font_family": f"{Font.PRIMARY}, {Font.DEFAULT}",
        "color": Color.PRIMARY_CONTENT,
        "margin_bottom": "0.5em",
        "line_height": "1.2",
    },
    rx.text: {
        **TextStyles.BODY,
        "color": Color.CONTENT,
    },
    rx.heading: {
        **TextStyles.HEADING,
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
        "background_color": Color.ACCENT,
        "color": "white",
        "font_family": Font.PRIMARY,
        "font_weight": "600",
        "font_size": FontSizes.BASE,  # 1rem / 16px
        "padding": "0.75rem 1.5rem",
        "border_radius": "0.5rem",
        "border": "none",
        "cursor": "pointer",
        "transition": "all 0.2s ease-in-out",
        "_hover": {
            "background_color": Color.ACCENT_LIGHT,
            "transform": "translateY(-1px)",
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
        },
        "_active": {
            "transform": "translateY(0)",
        },
        "_disabled": {
            "opacity": 0.6,
            "cursor": "not-allowed",
            "transform": "none",
            "box_shadow": "none",
        },
    },
    rx.input: {
        "font_family": Font.SECONDARY,
        "font_size": FontSizes.BASE,  # 1rem / 16px
        "padding": "0.75rem 1rem",
        "border_radius": "0.5rem",
        "border": f"1px solid {Color.BORDER}",
        "background": "white",
        "width": "100%",
        "transition": "all 0.2s ease-in-out",
        "_focus": {
            "border_color": Color.ACCENT,
            "box_shadow": f"0 0 0 1px {Color.ACCENT}",
            "outline": "none",
        },
        "_hover": {
            "border_color": Color.ACCENT_LIGHT,
        },
        "_placeholder": {
            "color": "gray.400",
            "font_size": FontSizes.SM,  # 0.875rem / 14px
        },
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