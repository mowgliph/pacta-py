from typing import Optional
import reflex as rx
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
from functools import wraps
import time
import os
import secrets

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora
CSRF_TOKEN_EXPIRE_HOURS = 24  # 24 horas
LOGIN_ATTEMPT_LIMIT = 5  # Número máximo de intentos de inicio de sesión
LOGIN_ATTEMPT_WINDOW = 900  # 15 minutos en segundos

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Almacenamiento en memoria para rate limiting
login_attempts = {}
csrf_tokens = set()

def csrf_protect(fn):
    """Decorator for CSRF protection on state handlers."""
    @wraps(fn)
    async def wrapper(self, *args, **kwargs):
        # Skip CSRF check for GET requests
        if self.router.method == "GET":
            return await fn(self, *args, **kwargs)
            
        # Get CSRF token from headers
        csrf_token = self.router.headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token not in csrf_tokens:
            self.error = "Invalid or missing CSRF token"
            return
            
        # Remove used token (one-time use)
        csrf_tokens.discard(csrf_token)
        return await fn(self, *args, **kwargs)
    return wrapper

def rate_limit(fn):
    """Decorator for rate limiting."""
    @wraps(fn)
    async def wrapper(self, *args, **kwargs):
        # Get client IP
        client_ip = self.router.client_ip
        
        # Clean up old attempts
        current_time = time.time()
        if client_ip in login_attempts:
            login_attempts[client_ip] = [
                attempt_time for attempt_time in login_attempts[client_ip]
                if current_time - attempt_time < LOGIN_ATTEMPT_WINDOW
            ]
        
        # Check if rate limit exceeded
        if len(login_attempts.get(client_ip, [])) >= LOGIN_ATTEMPT_LIMIT:
            self.error = "Too many login attempts. Please try again later."
            return
            
        # Record this attempt
        if client_ip not in login_attempts:
            login_attempts[client_ip] = []
        login_attempts[client_ip].append(current_time)
        
        return await fn(self, *args, **kwargs)
    return wrapper

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
    show_password: bool = False
    redirect_to: str = ""  # New state variable to handle redirects

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_db()
        self.load_token()

    def load_token(self):
        """Cargar el token desde las cookies."""
        try:
            # In Reflex, cookies are available in the request object
            request = self.get_request()
            if not request:
                return
                
            token = request.cookies.get("auth_token")
            if token and token != "":
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    self.username = payload.get("sub")
                    self.is_authenticated = True
                    self.remember_me = True
                    self.token = token
                except PyJWTError:
                    self.clear_auth_state()
        except Exception as e:
            print(f"Error loading token: {e}")
            self.clear_auth_state()

    def toggle_show_password(self):
        """Cambia la visibilidad de la contraseña."""
        self.show_password = not self.show_password

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
        
    def generate_csrf_token(self) -> str:
        """Generate a CSRF token and store it."""
        token = secrets.token_urlsafe(32)
        csrf_tokens.add(token)
        # Schedule token expiration
        rx.call_later(
            CSRF_TOKEN_EXPIRE_HOURS * 3600,
            lambda: csrf_tokens.discard(token)
        )
        return token

    def handle_submit(self, form_data: dict):
        """Handle form submission."""
        # Call login and handle the result
        login_result = self.login()
        if login_result:  # If login was successful
            self.is_authenticated = True
            # The UI will handle the redirect based on is_authenticated

    @csrf_protect
    @rate_limit
    async def login(self):
        """Handle user login.
        Returns:
            bool: True if login was successful, False otherwise
        """
        self.is_loading = True
        self.error = None
        
        try:
            db = next(get_db())
            user = db.query(UserModel).filter(UserModel.username == self.username).first()
            
            if user and bcrypt.checkpw(self.password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # Set user info (don't set is_authenticated here, let handle_submit do it)
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
                
                # Guardar token en cookies usando la respuesta
                response = self.get_response()
                if response:
                    response.set_cookie(
                        key="auth_token",
                        value=token,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        path="/",
                        secure=False,  # Cambiar a True en producción con HTTPS
                        httponly=True,
                        samesite="lax"
                    )
                
                # Limpiar la contraseña después de un inicio de sesión exitoso
                self.password = ""
                
                # Return True to indicate success
                return True
                
            else:
                self.error = "Usuario o contraseña incorrectos"
                return False
                
        except Exception as e:
            self.error = f"Error al iniciar sesión: {str(e)}"
            return ""
            
        finally:
            self.is_loading = False
# Focus management should be handled by UI components

    @csrf_protect
    @rate_limit
    async def register(self):
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
            
            # Guardar token en cookies usando la respuesta
            response = self.get_response()
            if response:
                response.set_cookie(
                    key="auth_token",
                    value=token,
                    max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    path="/",
                    secure=False,  # Cambiar a True en producción con HTTPS
                    httponly=True,
                    samesite="lax"
                )
        except IntegrityError:
            self.error = "Username or email already exists"
        except Exception as e:
            self.error = str(e)
        finally:
            self.is_loading = False

    def clear_auth_state(self):
        """Clear authentication state."""
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        self.email = ""
        self.user = None
        self.error = None
        self.token = None
        self.remember_me = False

    def logout(self):
        """Handle user logout."""
        # Clear auth state
        self.clear_auth_state()
        
        # Clear the auth token cookie by setting it to expire
        response = self.get_response()
        if response:
            response.delete_cookie(
                key="auth_token",
                path="/",
                secure=False,  # Cambiar a True en producción con HTTPS
                httponly=True,
                samesite="lax"
            )
