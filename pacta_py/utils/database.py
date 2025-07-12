from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pacta_py.models.user import Base, UserModel
from sqlalchemy.orm import Session
import bcrypt

SQLALCHEMY_DATABASE_URL = "sqlite:///./pacta.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializar la base de datos y crear usuario administrador si no existe."""
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Verificar si ya existe un admin y crearlo si no existe
    db = SessionLocal()
    try:
        admin = db.query(UserModel).filter_by(username="admin").first()
        if not admin:
            # Crear usuario admin
            password = "admin123"  # Cambia esto por una contraseña más segura en producción
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            admin_user = UserModel(
                username="admin",
                email="admin@pacta.app",
                password_hash=password_hash.decode('utf-8')
            )
            
            db.add(admin_user)
            db.commit()
            print("Usuario administrador creado exitosamente!")
    except Exception as e:
        print(f"Error al crear el usuario administrador: {str(e)}")
    finally:
        db.close()

def get_db():
    """Obtener una sesión de la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
