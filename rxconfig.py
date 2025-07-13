import reflex as rx

config = rx.Config(
    app_name="pacta",
    backend_packages=["bcrypt", "sqlalchemy", "python-jose[cryptography]", "passlib"],
    backend_port=8000,
    frontend_port=3000,
    api_url="http://localhost:8000",
    db_url="sqlite:///./pacta.db",
    env_path=".env",
    log_level="INFO",
    log_style="pretty",
    log_file=None,
    telemetry_enabled=False,
)
