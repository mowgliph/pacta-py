import reflex as rx
from .state.auth_state import AuthState
from .pages.login import login
from .pages.dashboard import dashboard as dashboard_page
from .utils.database import init_db
from .styles.styles import global_styles, Color

# Inicializar la base de datos al iniciar la aplicación
init_db()

# Configurar las rutas de la aplicación
def index():
    return rx.cond(
        AuthState.is_authenticated,
        dashboard_page(),
        login()
    )

def dashboard():
    return rx.cond(
        AuthState.is_authenticated,
        dashboard_page(),
        login()
    )

# Crear la aplicación
app = rx.App(
    style=global_styles,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="blue",
    )
)

# Añadir páginas con autenticación requerida para las rutas protegidas
app.add_page(index, route="/", title="PACTA - Login")
app.add_page(login, route="/login", title="PACTA - Login")
app.add_page(dashboard, route="/dashboard", title="PACTA - Dashboard")
