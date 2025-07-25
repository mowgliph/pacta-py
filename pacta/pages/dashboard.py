import reflex as rx
from pacta.state.auth_state import AuthState
from pacta.components.layout_base import LayoutBase
from pacta.styles.styles import Color

def dashboard():
    return LayoutBase(
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.text("Bienvenido/a, ", font_size="2xl", color=Color.CONTENT),
                    rx.text(
                        rx.cond(AuthState.user, AuthState.user.username, ""), 
                        font_size="2xl", 
                        color=Color.ACCENT,
                        font_weight="600"
                    ),
                ),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    background_color=Color.ERROR,
                    color=Color.WHITE,
                    _hover={"background_color": "#E63946"},
                ),
                rx.divider(border_color=Color.BORDER),
                rx.heading(
                    "Panel de Control", 
                    size="1",
                    color=Color.PRIMARY_CONTENT,
                    margin_bottom="1rem"
                ),
                rx.text(
                    "Esta es tu página de dashboard. Aquí podrás gestionar tus datos de PACTA.",
                    color=Color.SECONDARY_CONTENT
                ),
                spacing="4",
                padding="2rem",
            ),
            width="100%",
            max_width="1200px",
            margin_x="auto",
            padding="2rem 1rem",
            background_color=Color.WHITE,
            border_radius="0.5rem",
            box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        )
    )
