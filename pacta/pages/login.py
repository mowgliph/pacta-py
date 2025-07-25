import reflex as rx
from ..state.auth_state import AuthState
from ..styles.styles import Color, Font, TextStyles
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

input_container_style = {
    "width": "100%",
    "margin_bottom": "1.25rem",
}

password_input_style = {
    "padding_right": "2.5rem",  # Space for the eye icon
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
                    font_size="1.125rem",
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
                        AuthState.error != "",
                        alert(
                            title="Error",
                            description=AuthState.error,
                            status=AlertType.ERROR,
                            margin_bottom="1.5rem",
                            on_close=AuthState.clear_error,
                        ),
                    ),
                    
                    # Username field
                    rx.vstack(
                        rx.text(
                            "Usuario",
                            color=Color.SECONDARY_CONTENT, 
                            align_self="start",
                            font_size=TextStyles.SMALL["font_size"],
                            font_weight="500",
                            font_family=Font.PRIMARY,
                            margin_bottom="0.5rem",
                        ),
                        rx.hstack(
                            rx.icon(tag="user", color=Color.ACCENT, size=20, margin_right="0.5rem"),
                            rx.input(
                                placeholder="usuario@ejemplo.com",
                                value=AuthState.username,
                                on_change=AuthState.set_username,
                                variant="surface",
                                padding_y="0.75rem",
                                _placeholder={"color": "gray.400"},
                                border="none",
                                _focus={
                                    "box_shadow": "none",
                                    "outline": "none"
                                },
                            ),
                            spacing="3",
                            padding_x="0.75rem",
                            border_radius="md",
                            border=f"1px solid {Color.BORDER}",
                            _hover={"border_color": Color.ACCENT_LIGHT},
                            **input_container_style,
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
                            font_size=TextStyles.SMALL["font_size"],
                            font_weight="500",
                            font_family=Font.PRIMARY,
                            margin_bottom="0.5rem",
                            margin_top="1rem",
                        ),
                        rx.box(
                            position="relative",
                            width="100%",
                        )[
                            rx.hstack(
                                rx.icon(tag="lock", color=Color.ACCENT, size=20),
                                rx.input(
                                    placeholder="••••••••",
                                    type_=rx.cond(AuthState.show_password, "text", "password"),
                                    value=AuthState.password,
                                    on_change=AuthState.set_password,
                                    variant="surface",
                                    padding_y="0.75rem",
                                    border="none",
                                    _placeholder={"color": "gray.400"},
                                    _focus={
                                        "box_shadow": "none",
                                        "outline": "none"
                                    },
                                    **password_input_style,
                                ),
                                rx.button(
                                    rx.icon(
                                        tag=rx.cond(AuthState.show_password, "eye-off", "eye"),
                                        size=16,
                                        color=Color.SECONDARY_CONTENT,
                                    ),
                                    on_click=AuthState.toggle_show_password,
                                    **show_password_button_style,
                                ),
                                spacing="3",
                                padding_x="0.75rem",
                                border_radius="md",
                                border=f"1px solid {Color.BORDER}",
                                _hover={"border_color": Color.ACCENT_LIGHT},
                                align_items="center",
                            ),
                        ],
                        spacing="1",
                        width="100%",
                        align_items="start",
                    ),
                    # Remember me
                    rx.checkbox(
                        rx.text(
                            "Recordarme",
                            color=Color.SECONDARY_CONTENT,
                            font_size=TextStyles.SMALL["font_size"],
                            font_family=Font.PRIMARY,
                            font_weight="500",
                            margin_left="0.5rem",
                        ),
                        on_change=AuthState.set_remember_me,
                        size="md",
                        color_scheme=Color.ACCENT[1:],  # Elimina el # del color
                        _hover={"border_color": Color.ACCENT},
                        margin_top="0.5rem",
                        border_color=Color.BORDER,
                    ),
                    
                    # Login button
                    rx.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.spinner(color="white", size="sm"),
                            "Iniciar sesión",
                        ),
                        type_="submit",
                        width="100%",
                        size="lg",
                        is_loading=AuthState.is_loading,
                        is_disabled=rx.cond(
                            (AuthState.username == "") | (AuthState.password == ""),
                            True,
                            False,
                        ),
                        background=Color.ACCENT,
                        color=Color.WHITE,
                        _hover={
                            "opacity": "0.9",
                            "transform": "translateY(-1px)",
                            "box_shadow": "0 4px 12px rgba(70, 143, 175, 0.2)",
                        },
                        _active={
                            "opacity": "0.8",
                            "transform": "translateY(0)",
                            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                        },
                        margin_top="1.5rem",
                        font_weight="500",
                        font_family=Font.PRIMARY,
                    ),
                    
                    # Redirect is handled by the handle_submit method
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.script("window.location.href = '/dashboard'"),
                        rx.box(),
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                on_submit=AuthState.handle_submit,
                width="100%",
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
