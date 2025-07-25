import reflex as rx
from ..styles.styles import Color, TextStyles, Font

class AlertType:
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

# Mapeo de tipos de alerta a estilos basados en la paleta global
alert_styles = {
    AlertType.SUCCESS: {
        "bg": "rgba(167, 201, 87, 0.1)",
        "border_color": Color.SUCCESS,
        "icon": "badge-check",  # Available in Reflex
        "color": "#2b5a1e",
    },
    AlertType.ERROR: {
        "bg": "rgba(255, 99, 71, 0.1)",
        "border_color": "#FF6347",
        "icon": "badge-minus",  # Using x_circle as alternative to alert_circle
        "color": "#8B1A1A",
    },
    AlertType.WARNING: {
        "bg": "rgba(242, 232, 109, 0.15)",
        "border_color": Color.WARNING,
        "icon": "badge-alert",  # This is available in Reflex
        "color": "#8B6914",
    },
    AlertType.INFO: {
        "bg": "rgba(73, 160, 255, 0.1)",
        "border_color": Color.ACCENT,
        "icon": "badge-info",  # This is available in Reflex
        "color": Color.PRIMARY_CONTENT,
    },
}

def alert(
    title: str = None,
    description: str = None,
    status: str = AlertType.INFO,
    show_icon: bool = True,
    is_closable: bool = True,
    on_close=None,
    **props
) -> rx.Component:
    """
    Componente de alerta personalizado que utiliza la paleta de colores global.
    
    Args:
        title: Título de la alerta (opcional)
        description: Descripción de la alerta (opcional)
        status: Tipo de alerta (success, error, warning, info)
        show_icon: Mostrar icono
        is_closable: Permitir cerrar la alerta
        on_close: Función a ejecutar al cerrar la alerta
        **props: Propiedades adicionales para personalización
        
    Returns:
        Componente de alerta de Reflex
    """
    """
    Componente de alerta personalizado.
    
    Args:
        title: Título de la alerta (opcional)
        description: Descripción de la alerta (opcional)
        status: Tipo de alerta (success, error, warning, info)
        show_icon: Mostrar icono
        is_closable: Permitir cerrar la alerta
        on_close: Función a ejecutar al cerrar la alerta
        **props: Propiedades adicionales
        
    Returns:
        Componente de alerta de Reflex
    """
    status = status.lower()
    styles = alert_styles.get(status, alert_styles[AlertType.INFO])
    
    # Estilo base para el contenedor de la alerta
    alert_container_style = {
        "width": "100%",
        "margin_bottom": "1rem",
        "font_family": Font.SECONDARY,
        "transition": "all 0.2s ease-in-out",
    }
    
    # Estilo para el contenido de la alerta
    content_style = {
        "align_items": "flex-start",
        "padding": "1rem",
        "border_radius": "0.5rem",
        "border_left": f"4px solid {styles['border_color']}",
        "background_color": styles["bg"],
        "width": "100%",
        "box_shadow": "0 1px 3px 0 rgba(0, 0, 0, 0.05)",
    }
    
    # Aplicar estilos personalizados adicionales si se proporcionan
    if "style" in props:
        content_style.update(props.pop("style"))
    
    return rx.box(
        rx.hstack(
            # Icono
            rx.cond(
                show_icon,
                rx.icon(
                    tag=styles["icon"],
                    color=styles["color"],
                    margin_right="0.75rem",
                    flex_shrink=0,
                    size=20,
                ),
                None,
            ),
            
            # Contenido
            rx.vstack(
                rx.cond(
                    title,
                    rx.text(
                        title,
                        color=styles["color"],
                        margin_bottom=rx.cond(description, "0.25rem", "0"),
                        font_family=Font.PRIMARY,
                        font_weight="600",
                        line_height="1.3",
                    ),
                    None,
                ),
                rx.cond(
                    description,
                    rx.text(
                        description,
                        color=styles["color"],
                        opacity=0.9,
                        **TextStyles.BODY,
                        font_size="0.9375rem",  # Tamaño ligeramente más pequeño para la descripción
                    ),
                    None,
                ),
                align_items="flex-start",
                spacing="0",
                width="100%",
            ),
            
            # Botón de cierre
            rx.cond(
                is_closable,
                rx.button(
                    rx.icon(
                        tag="octagon-x",  # Using x_mark instead of x
                        size=16,
                    ),
                    on_click=on_close,
                    variant="ghost",
                    size="1",  # Using valid size value (1-4)
                    color=styles["color"],
                    _hover={"background": "transparent", "opacity": "0.8"},
                    _active={"background": "transparent"},
                    padding="0.25rem",
                    height="auto",
                ),
                None,
            ),
            
            **content_style,
            **props,
        ),
        **alert_container_style,
    )
