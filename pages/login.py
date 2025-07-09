from reflex import el
from state.auth_state import AuthState

def login():
    return el.center(
        el.vstack(
            el.heading("PACTA - Login", size="xl"),
            el.input(
                placeholder="Username",
                on_change=AuthState.set_username,
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
            el.checkbox(
                "Recordarme",
                on_change=AuthState.set_remember_me,
            ),
            el.button(
                "Login",
                on_click=AuthState.login,
                width="100%",
                max_width="400px",
                is_loading=AuthState.is_loading,
            ),
            el.text(
                AuthState.error if AuthState.error else "",
                color="red",
            ),
            el.link(
                "¿No tienes cuenta? Regístrate aquí",
                href="/register",
                color="blue",
            ),
            spacing="1rem",
            padding="2rem",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
    )
