import reflex as rx
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

try:
    config = rx.Config(
        app_name="pacta",
        backend_packages=["bcrypt", "sqlalchemy", "python-jose[cryptography]", "passlib"],
        backend_port=os.getenv("BACKEND_PORT"),
        frontend_port=os.getenv("FRONTEND_PORT"),
        api_url=f"{os.getenv('API_URL')}:{os.getenv('FRONTEND_PORT')}",
        db_url=os.getenv("DB_URL"),
        env_path=".env",
        log_level="INFO",
        log_style="pretty",
        log_file=None,
        telemetry_enabled=False,
    )
except Exception as e:
    print(f"Error al configurar Reflex: {e}")
