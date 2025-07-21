import reflex as rx
from pacta.state.auth_state import AuthState
from pacta.pages.login import login
from pacta.pages.dashboard import dashboard as dashboard_page
from pacta.utils.database import init_db
from pacta.styles.styles import global_styles

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
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap"
    ]
)
app.add_page(index, route="/", title="PACTA - Login")
app.add_page(login, route="/login", title="PACTA - Login")
app.add_page(dashboard, route="/dashboard", title="PACTA - Dashboard")
