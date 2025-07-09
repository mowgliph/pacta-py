from reflex import el
from state.auth_state import AuthState

def dashboard():
    return el.center(
        el.vstack(
            el.hstack(
                el.text("Bienvenido/a, ", font_size="2xl"),
                el.text(AuthState.user.username if AuthState.user else "", font_size="2xl", color="blue"),
            ),
            el.button(
                "Cerrar Sesión",
                on_click=AuthState.logout,
                bg_color="red",
                color="white",
            ),
            el.divider(),
            el.heading("Panel de Control", size="xl"),
            el.text("Esta es tu página de dashboard. Aquí podrás gestionar tus datos de PACTA."),
            spacing="1rem",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
