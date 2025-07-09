from reflex import el
from state.auth_state import AuthState

def register():
    return el.center(
        el.vstack(
            el.heading("PACTA - Registro", size="xl"),
            el.input(
                placeholder="Username",
                on_change=AuthState.set_username,
                width="100%",
                max_width="400px",
            ),
            el.input(
                placeholder="Email",
                on_change=AuthState.set_email,
                width="100%",
                max_width="400px",
            ),
            el.input(
                placeholder="Password",
                type_="password",
                on_change=AuthState.set_password,
                width="100%",
                max_width="400px",
            ),
            el.button(
                "Registrar",
                on_click=AuthState.register,
                width="100%",
                max_width="400px",
                is_loading=AuthState.is_loading,
            ),
            el.text(
                AuthState.error if AuthState.error else "",
                color="red",
            ),
            el.link(
                "¿Ya tienes cuenta? Inicia sesión aquí",
                href="/login",
                color="blue",
            ),
            spacing="1rem",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
