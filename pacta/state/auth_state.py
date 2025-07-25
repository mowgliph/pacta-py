from typing import Optional, Dict, List, Tuple, Callable, Any, Union
import reflex as rx
from reflex import State
from pacta.models.user import User, UserModel, UserCreate
from pacta.utils.database import get_db, init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import bcrypt
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from functools import wraps
import time
import os
import secrets
import re
import logging
from email_validator import validate_email, EmailNotValidError
from typing_extensions import TypedDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions
class LoginAttempt(TypedDict):
    attempts: int
    last_attempt: float
    locked_until: Optional[float]

class PasswordRequirements(TypedDict):
    min_length: int
    require_uppercase: bool
    require_lowercase: bool
    require_digits: bool
    require_special_chars: bool

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or SECRET_KEY == "your-secret-key-change-this-in-production":
    raise ValueError("SECRET_KEY must be set in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days
CSRF_TOKEN_EXPIRE_HOURS = 24  # 24 hours
LOGIN_ATTEMPT_LIMIT = 5  # Max login attempts
LOGIN_ATTEMPT_WINDOW = 900  # 15 minutes in seconds
ACCOUNT_LOCKOUT_MINUTES = 30  # 30 minutes lockout after max attempts
PASSWORD_RESET_EXPIRE_HOURS = 1  # 1 hour for password reset

# Password requirements
PASSWORD_REQUIREMENTS: PasswordRequirements = {
    "min_length": 12,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digits": True,
    "require_special_chars": True
}

# Rate limiting configuration
RATE_LIMITS = {
    "login": (5, 60),  # 5 requests per minute
    "register": (3, 300),  # 3 requests per 5 minutes
    "password_reset": (3, 3600)  # 3 requests per hour
}

# Security utilities
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Increased work factor for better security
)

# In-memory storage for security features
login_attempts: Dict[str, LoginAttempt] = {}
csrf_tokens: Dict[str, float] = {}  # token -> expiration timestamp
rate_limits: Dict[str, Dict[str, List[float]]] = {}  # endpoint -> {ip: [timestamps]}
password_reset_tokens: Dict[str, Tuple[str, float]] = {}  # token -> (email, expiration)

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password against complexity requirements."""
    if len(password) < PASSWORD_REQUIREMENTS["min_length"]:
        return False, f"Password must be at least {PASSWORD_REQUIREMENTS['min_length']} characters long"
    
    if PASSWORD_REQUIREMENTS["require_uppercase"] and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
        
    if PASSWORD_REQUIREMENTS["require_lowercase"] and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
        
    if PASSWORD_REQUIREMENTS["require_digits"] and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
        
    if PASSWORD_REQUIREMENTS["require_special_chars"] and not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character"
        
    return True, ""

def validate_email_format(email: str) -> Tuple[bool, str]:
    """Validate email format using email-validator."""
    try:
        validate_email(email, check_deliverability=False)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)

def is_rate_limited(endpoint: str, ip: str) -> Tuple[bool, Optional[float]]:
    """Check if the IP is rate limited for the given endpoint."""
    if endpoint not in RATE_LIMITS:
        return False, None
        
    max_requests, time_window = RATE_LIMITS[endpoint]
    current_time = time.time()
    
    # Initialize rate limit tracking for this endpoint and IP
    if endpoint not in rate_limits:
        rate_limits[endpoint] = {}
    if ip not in rate_limits[endpoint]:
        rate_limits[endpoint][ip] = []
    
    # Clean up old requests
    rate_limits[endpoint][ip] = [
        t for t in rate_limits[endpoint][ip]
        if current_time - t < time_window
    ]
    
    # Check if rate limit exceeded
    if len(rate_limits[endpoint][ip]) >= max_requests:
        retry_after = rate_limits[endpoint][ip][0] + time_window - current_time
        return True, max(0, retry_after)
    
    # Record this request
    rate_limits[endpoint][ip].append(current_time)
    return False, None

def csrf_protect(fn: Callable) -> Callable:
    """Decorator for CSRF protection on state handlers.
    
    This version is compatible with the current Reflex router implementation.
    
    Args:
        fn: The function to protect with CSRF checks
        
    Returns:
        The wrapped function with CSRF protection
    """
    @wraps(fn)
    async def wrapper(self, *args, **kwargs):
        try:
            # Skip CSRF check for safe methods if we can determine the method
            if hasattr(self, 'router') and hasattr(self.router, 'headers'):
                method = self.router.headers.get("x-method", "").upper()
                if method in ("GET", "HEAD", "OPTIONS"):
                    return await fn(self, *args, **kwargs)
            
            # Get CSRF token from headers or form data
            csrf_token = None
            if hasattr(self, 'router') and hasattr(self.router, 'headers'):
                csrf_token = self.router.headers.get("x-csrf-token") or \
                           self.router.headers.get("x-xsrf-token")
                
                # If no token in headers, check form data (for form submissions)
                if not csrf_token and hasattr(self, 'router') and hasattr(self.router, 'form_data'):
                    csrf_token = self.router.form_data.get("csrf_token")
            
            current_time = time.time()
            
            # Validate CSRF token
            if not csrf_token or csrf_token not in csrf_tokens:
                logger.warning("CSRF token validation failed: token missing or invalid")
                self.error = "Solicitud no válida. Por favor, recarga la página e intenta de nuevo."
                return None
                
            # Check if token is expired
            if csrf_tokens[csrf_token] < current_time:
                logger.warning("CSRF token expired")
                if csrf_token in csrf_tokens:
                    del csrf_tokens[csrf_token]
                self.error = "La sesión ha expirado. Por favor, recarga la página."
                return None
                
            # Remove used token (one-time use)
            if csrf_token in csrf_tokens:
                del csrf_tokens[csrf_token]
            logger.debug("CSRF token validated successfully")
            
            # Call the original function
            return await fn(self, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in CSRF protection: {e}", exc_info=True)
            self.error = "Error de seguridad. Por favor, inténtalo de nuevo."
            return None
    return wrapper

def rate_limit(endpoint: str) -> Callable:
    """Decorator factory for rate limiting specific endpoints.
    
    Args:
        endpoint: The endpoint name to apply rate limiting to
        
    Returns:
        A decorator that applies rate limiting to the wrapped function
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        async def wrapper(self, *args, **kwargs):
            try:
                client_ip = self.router.client_ip
                
                # Check if IP is rate limited for this endpoint
                is_limited, retry_after = is_rate_limited(endpoint, client_ip)
                if is_limited:
                    minutes = int(retry_after // 60) if retry_after else 1
                    self.error = (
                        f"Demasiadas solicitudes. Por favor, espera {minutes} minutos e inténtalo de nuevo."
                    )
                    logger.warning(f"Rate limit exceeded for {endpoint} from {client_ip}")
                    return None
                
                return await fn(self, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Error in rate limiting for {endpoint}: {e}", exc_info=True)
                self.error = "Error de límite de tasa. Por favor, inténtalo de nuevo más tarde."
                return None
        return wrapper
    return decorator

class AuthState(State):
    # Login state
    username: str = ""
    password: str = ""
    show_password: bool = False
    remember_me: bool = False
    is_authenticated: bool = False
    is_loading: bool = False
    error: Optional[str] = None
    success: Optional[str] = None
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[User] = None
    redirect_to: str = ""
    
    # Password reset
    reset_token: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_db()
        self.load_token()

    def load_token(self):
        """Load token from cookies."""
        try:
            # In Reflex, cookies are available through the router
            if not hasattr(self, 'router') or not hasattr(self.router, 'cookies'):
                return
                
            token = self.router.cookies.get("access_token")
            if not token:
                token = self.router.cookies.get("auth_token")  # Fallback to legacy cookie
                
            if token:
                try:
                    payload = jwt.decode(
                        token,
                        SECRET_KEY,
                        algorithms=[ALGORITHM],
                        options={"verify_exp": False}  # Don't verify expiration here
                    )
                    self.username = payload.get("username") or payload.get("sub")
                    self.is_authenticated = True
                    self.remember_me = True
                    self.token = token
                    logger.debug("Successfully loaded token from cookies")
                except PyJWTError as e:
                    logger.warning(f"Invalid token in cookies: {e}")
                    self.clear_auth_state()
        except Exception as e:
            logger.error(f"Error loading token: {e}", exc_info=True)
            self.clear_auth_state()

    def toggle_show_password(self):
        """Toggle password visibility in the UI."""
        self.show_password = not self.show_password
        return self.show_password

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token.
        
        Args:
            data: The data to encode in the token
            expires_delta: Optional timedelta for token expiration
            
        Returns:
            str: Encoded JWT token
        """
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            to_encode.update({
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access"
            })
            return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        except Exception as e:
            logger.error(f"Error creating access token: {e}", exc_info=True)
            raise ValueError("Error al generar el token de acceso")
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token for the user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            str: Encoded JWT refresh token
        """
        try:
            return jwt.encode(
                {
                    "sub": user_id,
                    "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                    "iat": datetime.utcnow(),
                    "type": "refresh"
                },
                SECRET_KEY,
                algorithm=ALGORITHM
            )
        except Exception as e:
            logger.error(f"Error creating refresh token: {e}", exc_info=True)
            raise ValueError("Error al generar el token de actualización")
        
    def generate_csrf_token(self) -> str:
        """Generate and store a CSRF token with expiration.
        
        Returns:
            str: A new CSRF token
        """
        try:
            token = secrets.token_urlsafe(32)
            expiration = time.time() + (CSRF_TOKEN_EXPIRE_HOURS * 3600)
            csrf_tokens[token] = expiration
            
            # Clean up expired tokens
            current_time = time.time()
            expired = [t for t, exp in csrf_tokens.items() if exp < current_time]
            for t in expired:
                csrf_tokens.pop(t, None)
                
            logger.debug(f"Generated new CSRF token, {len(csrf_tokens)} active tokens")
            return token
            
        except Exception as e:
            logger.error(f"Error generating CSRF token: {e}", exc_info=True)
            raise ValueError("Error al generar el token de seguridad")

    def _is_account_locked_out(self, client_ip: str) -> bool:
        """Check if the account is locked out due to too many failed attempts.
        
        Args:
            client_ip: The client's IP address
            
        Returns:
            bool: True if the account is locked out, False otherwise
        """
        if client_ip not in login_attempts:
            return False
            
        attempt_data = login_attempts[client_ip]
        current_time = time.time()
        
        # Check if lockout period has expired
        if 'locked_until' in attempt_data and attempt_data['locked_until'] < current_time:
            del login_attempts[client_ip]
            return False
            
        # Check if max attempts reached
        return attempt_data.get('attempts', 0) >= LOGIN_ATTEMPT_LIMIT
    
    def _record_failed_attempt(self, client_ip: str) -> None:
        """Record a failed login attempt for the given IP."""
        current_time = time.time()
        
        # Initialize attempt tracking for this IP
        if client_ip not in login_attempts:
            login_attempts[client_ip] = {
                'attempts': 0,
                'last_attempt': current_time
            }
        
        # Increment attempt count and update timestamp
        login_attempts[client_ip]['attempts'] += 1
        login_attempts[client_ip]['last_attempt'] = current_time
        
        # Lock account if max attempts reached
        if login_attempts[client_ip]['attempts'] >= LOGIN_ATTEMPT_LIMIT:
            lockout_until = current_time + (ACCOUNT_LOCKOUT_MINUTES * 60)
            login_attempts[client_ip]['locked_until'] = lockout_until
            logger.warning(f"Account locked for IP {client_ip} until {datetime.fromtimestamp(lockout_until)}")
    
    def _reset_login_attempts(self, client_ip: str) -> None:
        """Reset login attempts for the given IP after successful login."""
        if client_ip in login_attempts:
            del login_attempts[client_ip]
    
    @csrf_protect
    @rate_limit("login")
    async def handle_submit(self, form_data: dict) -> bool:
        """Handle form submission and update authentication state.
        
        Args:
            form_data: Dictionary containing form data
            
        Returns:
            bool: True if login was successful, False otherwise
        """
        self.is_loading = True
        self.error = None
        self.success = None
        
        try:
            # Update state with form data
            if 'username' in form_data:
                self.username = form_data['username']
            if 'password' in form_data:
                self.password = form_data['password']
            if 'remember_me' in form_data:
                self.remember_me = form_data['remember_me']
            
            # Validate inputs
            if not self.username or not self.password:
                self.error = "Por favor ingresa tu usuario y contraseña"
                self.is_loading = False
                return False
                
            # Get client IP for rate limiting
            client_ip = getattr(getattr(self, 'router', None), 'client_ip', 'unknown')
            
            # Check account lockout status
            if self._is_account_locked_out(client_ip):
                lockout_time = login_attempts.get(client_ip, {}).get('locked_until', 0)
                remaining_time = int((lockout_time - time.time()) / 60) + 1
                self.error = f"Demasiados intentos fallidos. Intenta de nuevo en {remaining_time} minutos."
                self.is_loading = False
                return False
            
            db = next(get_db())
            user = db.query(UserModel).filter(UserModel.username == self.username).first()
            
            # Verify user exists and is active
            if not user:
                self._record_failed_attempt(client_ip)
                self.error = "Usuario o contraseña incorrectos"
                self.is_loading = False
                return False
                
            if not user.is_active:
                self.error = "Esta cuenta ha sido desactivada. Por favor contacta al administrador."
                self.is_loading = False
                return False
                
            # Verify password
            try:
                if not pwd_context.verify(self.password, user.password_hash):
                    self._record_failed_attempt(client_ip)
                    remaining_attempts = LOGIN_ATTEMPT_LIMIT - login_attempts.get(client_ip, {}).get('attempts', 0)
                    
                    if remaining_attempts > 0:
                        self.error = f"Usuario o contraseña incorrectos. Te quedan {remaining_attempts} intentos."
                    else:
                        self.error = "Demasiados intentos fallidos. Tu cuenta ha sido bloqueada temporalmente."
                    
                    self.is_loading = False
                    return False
                    
            except Exception as e:
                logger.error(f"Password verification error for user {self.username}: {e}")
                self.error = "Error al verificar las credenciales. Por favor intenta de nuevo."
                self.is_loading = False
                return False
            
            
        except SQLAlchemyError as e:
            logger.error(f"Database error during login: {e}")
            self.error = "Error al acceder a la base de datos. Por favor intenta de nuevo."
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}", exc_info=True)
            self.error = "Ocurrió un error inesperado. Por favor intenta de nuevo más tarde."
            return False
            
        finally:
            self.is_loading = False
            
    # Focus management should be handled by UI components

    def clear_auth_state(self) -> None:
        """Clear all authentication state and sensitive data."""
        try:
            self.is_authenticated = False
            self.user = None
            self.token = None
            self.refresh_token = None
            self.redirect_to = ""
            
            # Clear form fields
            self.username = ""
            self.password = ""
            
            # Clear UI state
            self.error = None
            self.success = None
            self.remember_me = False
            self.is_loading = False
            
        except Exception as e:
            logger.error(f"Error clearing auth state: {e}", exc_info=True)
            # Even if there's an error, we want to continue with logout
        
    def clear_error(self) -> bool:
        """Clear any error messages from the state.
        
        Returns:
            bool: Always returns True to indicate success to the frontend
        """
        self.error = None
        return True
        
    def clear_success(self) -> bool:
        """Clear any success messages from the state.
        
        Returns:
            bool: Always returns True to indicate success to the frontend
        """
        self.success = None
        return True

    def logout(self) -> None:
        """Handle user logout by clearing all authentication state and cookies."""
        try:
            # Clear auth state first
            self.clear_auth_state()
            
            # Get response object to clear cookies
            response = getattr(self, 'router', {}).get('session', {}).get('response')
            if response:
                # Clear access token cookie
                response.delete_cookie(
                    key="access_token",
                    path="/",
                    secure=os.getenv("ENV") == "production",
                    httponly=True,
                    samesite="lax",
                    domain=os.getenv("COOKIE_DOMAIN", None)
                )
                
                # Clear refresh token cookie
                response.delete_cookie(
                    key="refresh_token",
                    path="/",
                    secure=os.getenv("ENV") == "production",
                    httponly=True,
                    samesite="lax",
                    domain=os.getenv("COOKIE_DOMAIN", None)
                )
                
                # Clear any legacy cookies
                response.delete_cookie(
                    key="auth_token",
                    path="/",
                    secure=os.getenv("ENV") == "production",
                    httponly=True,
                    samesite="lax",
                    domain=os.getenv("COOKIE_DOMAIN", None)
                )
                
            logger.info(f"User logged out successfully: {self.user.username if self.user else 'unknown'}")
            return True
            
        except Exception as e:
            logger.error(f"Error during logout: {e}", exc_info=True)
            # Even if there's an error, we still want to clear the auth state
            self.clear_auth_state()
            return False