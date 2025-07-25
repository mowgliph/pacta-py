import reflex as rx
from ..styles.styles import Color, TextStyles

def footer() -> rx.Component:
    """
    Componente de pie de página reutilizable para la aplicación.
    
    Returns:
        rx.Component: Componente de pie de página
    """
    return rx.box(
        rx.hstack(
            rx.text(
                "© 2025 PACTA. Todos los derechos reservados.",
                color=Color.SECONDARY_CONTENT,
                **TextStyles.SMALL,
                style={
                    "opacity": "0.7",
                    "font_size": "0.75rem"
                }
            ),
            # Aquí podrías agregar más elementos como enlaces, redes sociales, etc.
            justify_content="center",
            width="100%",
            padding_y="1rem",
            border_top=f"1px solid {Color.BORDER}",
            margin_top="auto"  # Esto asegura que el footer se mantenga en la parte inferior
        ),
        width="100%",
        margin_top="2rem",
        style={
            "background_color": Color.WHITE,
            "box_shadow": "0 -2px 10px 0 rgba(0, 0, 0, 0.02)"
        }
    )
