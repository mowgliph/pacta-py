from typing import Optional
from reflex import State
from pacta.models.user import User, UserModel, UserCreate
from pacta.utils.database import get_db, init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

# Configuración para el token
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthState(State):
    username: str = ""
    password: str = ""
    email: str = ""
    is_loading: bool = False
    error: Optional[str] = None
    is_authenticated: bool = False
    user: Optional[User] = None
    remember_me: bool = False
    token: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_db()
        self.load_token()

    def load_token(self):
        """Cargar el token desde el almacenamiento."""
        try:
            token = self.get_local_storage("auth_token")
            if token:
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    self.username = payload.get("sub")
                    self.is_authenticated = True
                    self.remember_me = True
                except PyJWTError:
                    pass
        except Exception:
            pass

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Crear un token de acceso."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def login(self):
        """Handle user login."""
        self.is_loading = True
        self.error = None
        
        try:
            db = next(get_db())
            user = db.query(UserModel).filter(UserModel.username == self.username).first()
            
            if user and bcrypt.checkpw(self.password.encode('utf-8'), user.password_hash.encode('utf-8')):
                self.is_authenticated = True
                self.user = User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    created_at=user.created_at.isoformat() if user.created_at else None,
                    updated_at=user.updated_at.isoformat() if user.updated_at else None
                )
                
                # Crear token
                expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                token = self.create_access_token(data={"sub": self.username}, expires_delta=expire)
                self.token = token
                
                # Guardar token si remember_me está marcado
                if self.remember_me:
                    self.set_local_storage("auth_token", token)
            else:
                self.error = "Invalid credentials"
        except Exception as e:
            self.error = str(e)
        finally:
            self.is_loading = False

    def register(self):
        """Handle user registration."""
        self.is_loading = True
        self.error = None
        
        try:
            db = next(get_db())
            user_data = UserCreate(
                username=self.username,
                email=self.email,
                password=self.password
            )
            
            # Hash the password
            password_hash = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
            
            new_user = UserModel(
                username=user_data.username,
                email=user_data.email,
                password_hash=password_hash.decode('utf-8')
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            self.is_authenticated = True
            self.user = User.from_orm(new_user)
            
            # Crear token
            expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = self.create_access_token(data={"sub": self.username}, expires_delta=expire)
            self.token = token
            
            # Guardar token si remember_me está marcado
            if self.remember_me:
                self.set_local_storage("auth_token", token)
        except IntegrityError:
            self.error = "Username or email already exists"
        except Exception as e:
            self.error = str(e)
        finally:
            self.is_loading = False

    def logout(self):
        """Handle user logout."""
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        self.email = ""
        self.user = None
        self.error = None
        self.token = None
        self.set_local_storage("auth_token", "")
