import reflex as rx
from state.auth_state import AuthState
from pages.login import login
from pages.register import register
from pages.dashboard import dashboard
from utils.database import init_db

# Inicializar la base de datos al iniciar la aplicación
init_db()

# Función para proteger rutas
@rx.middleware
async def protect_routes(app: rx.App, request: rx.Request, response: rx.Response):
    """Middleware para proteger rutas."""
    if request.path in ["/dashboard"]:
        if not AuthState.is_authenticated:
            return rx.redirect("/login")
    return None

# Configurar las rutas de la aplicación
def index():
    return rx.cond(
        AuthState.is_authenticated,
        dashboard(),
        login()
    )

# Crear la aplicación
app = rx.App(state=AuthState, middleware=[protect_routes])
app.add_page(index, route="/", title="PACTA - Login")
app.add_page(login, route="/login", title="PACTA - Login")
app.add_page(register, route="/register", title="PACTA - Registro")
app.add_page(dashboard, route="/dashboard", title="PACTA - Dashboard")

# Compilar la aplicación
app.compile()
