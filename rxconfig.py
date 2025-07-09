import reflex as rx

# Configuración básica de la aplicación
config = rx.Config(
    app_name="pacta",
    frontend_packages=["@reflex-ui/core"],
    backend_packages=["bcrypt", "sqlalchemy", "python-jose[cryptography]", "passlib"],
    backend_port=8000,
    frontend_port=3000,
    api_url="http://localhost:8000",
    db_url="sqlite:///./pacta.db",
    env_path=".env",
    log_level="INFO",
    log_style="pretty",
    log_file=None,
    telemetry_enabled=False,  # Desactivada la telemetría
)
