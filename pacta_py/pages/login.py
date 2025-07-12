import reflex as rx
from pacta_py.state.auth_state import AuthState

def login():
    return rx.center(
        rx.vstack(
            rx.heading("PACTA - Login", size="1"),
            rx.input(
                placeholder="Username",
                on_change=AuthState.set_username,
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
            rx.checkbox(
                "Recordarme",
                on_change=AuthState.set_remember_me,
            ),
            rx.button(
                "Login",
                on_click=AuthState.login,
                width="100%",
                max_width="400px",
                is_loading=AuthState.is_loading,
            ),
            rx.text(
                rx.cond(AuthState.error, AuthState.error, ""),
                color="red",
            ),
            rx.link(
                "¿No tienes cuenta? Regístrate aquí",
                href="/register",
                color="blue",
            ),
            spacing="4",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
