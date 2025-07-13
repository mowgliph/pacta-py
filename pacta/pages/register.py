import reflex as rx
from pacta.state.auth_state import AuthState

def register():
    return rx.center(
        rx.vstack(
            rx.heading("PACTA - Registro", size="1"),
            rx.input(
                placeholder="Username",
                on_change=AuthState.set_username,
                width="100%",
                max_width="400px",
            ),
            rx.input(
                placeholder="Email",
                on_change=AuthState.set_email,
                width="100%",
                max_width="400px",
            ),
            rx.input(
                placeholder="Password",
                type_="password",
                on_change=AuthState.set_password,
                width="100%",
                max_width="400px",
            ),
            rx.button(
                "Registrar",
                on_click=AuthState.register,
                width="100%",
                max_width="400px",
                is_loading=AuthState.is_loading,
            ),
            rx.text(
                rx.cond(AuthState.error, AuthState.error, ""),
                color="red",
            ),
            rx.link(
                "¿Ya tienes cuenta? Inicia sesión aquí",
                href="/login",
                color="blue",
            ),
            spacing="4",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
