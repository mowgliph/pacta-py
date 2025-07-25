import reflex as rx
from ..styles.styles import Color


def Sidebar():
    return rx.box(
        rx.vstack(
            rx.heading(
                "PACTA", 
                size="4", 
                margin_bottom="2rem",
                color=Color.PRIMARY_CONTENT
            ),
            rx.link(
                "Estadísticas", 
                href="/estadisticas", 
                padding_y="1rem", 
                padding_x="1rem",
                width="100%",
                _hover={"background_color": Color.ACCENT_LIGHT, "border_radius": "0.375rem"},
                color=Color.CONTENT
            ),
            rx.link(
                "Contratos", 
                href="/contratos", 
                padding_y="1rem",
                padding_x="1rem",
                width="100%",
                _hover={"background_color": Color.ACCENT_LIGHT, "border_radius": "0.375rem"},
                color=Color.CONTENT
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        as_="nav",
        position="fixed",
        left="0",
        top="0",
        height="100vh",
        width="220px",
        background_color=Color.WHITE,
        padding="2rem 1rem",
        box_shadow="2px 0 8px rgba(0,0,0,0.04)",
        z_index="1000",
        border_right=f"1px solid {Color.BORDER}"
    )
