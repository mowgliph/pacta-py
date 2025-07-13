import reflex as rx
from pacta.state.auth_state import AuthState
from pacta.pages.login import login
from pacta.pages.register import register
from pacta.pages.dashboard import dashboard as dashboard_page
from pacta.utils.database import init_db

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
app = rx.App()
app.add_page(index, route="/", title="PACTA - Login")
app.add_page(login, route="/login", title="PACTA - Login")
app.add_page(register, route="/register", title="PACTA - Registro")
app.add_page(dashboard, route="/dashboard", title="PACTA - Dashboard")
