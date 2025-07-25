import reflex as rx
from ..state.auth_state import AuthState
from ..styles.styles import Color, Font, TextStyles, FontSizes
from ..components.alerts import alert, AlertType
from ..components.footer import footer

# Specific styles for login page
login_container_style = {
    "max_width": "450px",
    "width": "100%",
    "padding": "2.5rem",
    "background_color": Color.WHITE,
    "border_radius": "1rem",
    "box_shadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
    "border": f"1px solid {Color.BORDER}",
}

input_style = {
    "width": "100%",
    "padding": "0.5rem 0",
    "font_size": FontSizes.BASE,  # 1rem / 16px
    "line_height": "1.5",
    "min_height": "auto",
    "background": "transparent"
}

show_password_button_style = {
    "position": "absolute",
    "right": "0.75rem",
    "top": "50%",
    "transform": "translateY(-50%)",
    "background": "transparent",
    "border": "none",
    "cursor": "pointer",
    "padding": "0.25rem",
    "border_radius": "0.25rem",
    "_hover": {
        "background_color": "rgba(0, 0, 0, 0.05)",
    },
}

def login():
    return rx.center(
        rx.vstack(
            # Logo and Header
            rx.vstack(
                rx.heading(
                    "PACTA",
                    size="9",
                    background=f"linear-gradient(45deg, {Color.ACCENT}, {Color.PRIMARY})",
                    background_clip="text",
                    style={
                        "background_size": "200% auto",
                        "font_weight": "900",
                        "letter_spacing": "-0.025em",
                        "font_family": Font.PRIMARY,
                        "margin_bottom": "0.5rem",
                    },
                    animate="background-position 5s ease infinite",
                ),
                rx.text(
                    "Inicia sesión en tu cuenta",
                    color=Color.SECONDARY_CONTENT,
                    font_size=FontSizes.LG,  # 1.25rem / 20px
                    opacity="0.9",
                    margin_bottom="1.5rem",
                    font_family=Font.PRIMARY,
                ),
                spacing="1",
                align_items="center",
                width="100%",
            ),
            # Login Form
            rx.form(
                rx.vstack(
                    # Error message
                    rx.cond(
                        AuthState.error,
                        rx.callout(
                            AuthState.error,
                            icon="alert_triangle",
                            color_scheme="red",
                            variant="soft",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                    ),
                    # Success message
                    rx.cond(
                        AuthState.success,
                        rx.callout(
                            AuthState.success,
                            icon="check_circle",
                            color_scheme="green",
                            variant="soft",
                            width="100%",
                            margin_bottom="1rem"
                        ),
                    ),
                    # Username field
                    rx.vstack(
                        rx.text(
                            "Usuario",
                            color=Color.SECONDARY_CONTENT, 
                            align_self="start",
                            font_size=FontSizes.BASE,
                            font_weight="500",
                            font_family=Font.PRIMARY,
                            margin_bottom="0.5rem",
                        ),
                        rx.hstack(
                            rx.icon(
                                tag="user", 
                                color=Color.ACCENT, 
                                size=20, 
                                margin_right="0.5rem",
                                align_self="center"
                            ),
                            rx.input(
                                placeholder="usuario@ejemplo.com",
                                value=AuthState.username,
                                on_change=AuthState.set_username,
                                variant="classic",
                                border_color=Color.BORDER,
                                is_required=True,
                                error_border_color=Color.ERROR,
                                _focus={"border_color": Color.PRIMARY},
                                border_radius="0.375rem",
                                _placeholder={"color": "gray.400"},
                                _focus={
                                    "border_color": Color.ACCENT,
                                    "box_shadow": f"0 0 0 1px {Color.ACCENT}",
                                },
                                **input_style,
                            ),
                            spacing="1",
                            padding_x="0.25rem",
                        ),
                        spacing="1",
                        width="100%",
                        align_items="start",
                    ),
                    # Password field
                    rx.vstack(
                        rx.text(
                            "Contraseña",
                            color=Color.SECONDARY_CONTENT, 
                            align_self="start",
                            font_size=FontSizes.BASE,
                            font_weight="500",
                            font_family=Font.PRIMARY,
                            margin_bottom="0.5rem",
                            margin_top="1rem",
                        ),
                        rx.hstack(
                            rx.icon(
                                tag="lock",
                                size=16,
                                color=Color.ACCENT,
                                margin_right="0.5rem",
                                align_self="center"
                            ),
                            rx.hstack(
                                rx.input(
                                    placeholder="••••••••",
                                    value=AuthState.password,
                                    on_change=AuthState.set_password,
                                    type_="password" if not AuthState.show_password else "text",
                                    variant="classic",
                                    border_color=Color.BORDER,
                                    is_required=True,
                                    error_border_color=Color.ERROR,
                                    _focus={"border_color": Color.PRIMARY},
                                    padding_right="2.5rem",
                                    width="100%"
                                ),
                                rx.icon_button(
                                    rx.icon(
                                        tag="eye" if not AuthState.show_password else "eye-off",
                                        color=Color.SECONDARY_CONTENT,
                                        size=16
                                    ),
                                    on_click=AuthState.toggle_show_password,
                                    variant="ghost",
                                    size="sm",
                                    position="absolute",
                                    right="0.75rem",
                                    _hover={"background": "transparent"},
                                    aria_label="Toggle password visibility"
                                ),
                                position="relative",
                                width="100%"
                            ),
                            border_radius="0.375rem",
                            _placeholder={"color": "gray.400"},
                            _focus={
                                "border_color": Color.ACCENT,
                                "box_shadow": f"0 0 0 1px {Color.ACCENT}",
                            },
                        ),
                        spacing="1",
                        width="100%",
                        align_items="start",
                    ),
                    # Remember me
                    rx.hstack(
                        rx.checkbox(
                            "Recordar sesión",
                            is_checked=AuthState.remember_me,
                            on_change=AuthState.set_remember_me,
                            color_scheme=Color.PRIMARY,
                            size="sm",
                        ),
                        width="100%",
                        margin_bottom="1.5rem",
                    ),
                    # Login button
                    rx.button(
                        "Iniciar sesión",
                        type_="submit",
                        width="100%",
                        background_color=Color.PRIMARY,
                        color=Color.WHITE,
                        _hover={"opacity": "0.9"},
                        is_loading=AuthState.is_loading,
                        is_disabled=not (AuthState.username and AuthState.password),
                        loading_text="Iniciando sesión...",
                        font_weight="semibold",
                        height="2.75rem",
                        margin_bottom="1.5rem",
                        _active={
                            "opacity": "0.8",
                            "transform": "translateY(0)",
                            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                        },
                        margin_top="1.5rem",
                        font_weight="500",
                        font_family=Font.PRIMARY,
                    ),
                    
                    # Redirect is handled by the login method
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.script("window.location.href = '/dashboard'"),
                        rx.box(),
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                on_submit=AuthState.login,
                **login_container_style,
            ),
            
            spacing="6",
            width="100%",
            max_width="450px",
            padding_x="1rem",
        ),
        footer(),  # Agregando el componente Footer
        width="100%",
        min_height="100vh",
        padding_y="2rem",
        background_color=Color.BACKGROUND,
        style={
            "font_family": Font.DEFAULT,
            "background": f"linear-gradient(135deg, {Color.BACKGROUND} 0%, #f0f9ff 100%)",
            "display": "flex",
            "flex_direction": "column",
            "min_height": "100vh",
        },
    )
