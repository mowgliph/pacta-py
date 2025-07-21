import reflex as rx
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

try:
    config = rx.Config(
        app_name="pacta",
        backend_packages=["bcrypt", "sqlalchemy", "python-jose[cryptography]", "passlib"],
        db_url=os.getenv("DB_URL"),
        env_path=".env",
        log_level="INFO",
        log_style="pretty",
        log_file=None,
        telemetry_enabled=False,
        #plugins=["reflex.plugins.sitemap.SitemapPlugin"],
        #disable_plugins=[],
    )
except Exception as e:
    print(f"Error al configurar Reflex: {e}")
