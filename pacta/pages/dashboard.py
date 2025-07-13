import reflex as rx
from pacta.state.auth_state import AuthState

def dashboard():
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.text("Bienvenido/a, ", font_size="2xl"),
                rx.text(rx.cond(AuthState.user, AuthState.user.username, ""), font_size="2xl", color="blue"),
            ),
            rx.button(
                "Cerrar Sesión",
                on_click=AuthState.logout,
                bg_color="red",
                color="white",
            ),
            rx.divider(),
            rx.heading("Panel de Control", size="1"),
            rx.text("Esta es tu página de dashboard. Aquí podrás gestionar tus datos de PACTA."),
            spacing="4",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
