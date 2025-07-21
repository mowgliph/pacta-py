import reflex as rx
from pacta.state.auth_state import AuthState
from pacta.styles.styles import Color
from typing import Callable

def login():
    return rx.center(
        # Contenedor con aspecto de tarjeta
        rx.vstack(
            rx.box(
                rx.heading(
                    "PACTA",
                    size="8",
                    weight="bold",
                    text_align="center",
                    color=Color.PRIMARY_CONTENT,
                    margin_y="1rem",
                ),
                rx.text(
                    "Inicia sesión",
                    color=Color.SECONDARY_CONTENT,
                    text_align="center",
                    margin_y="1rem",
                ),
                padding_y="0.1rem",
                width="100%",
            ),
            rx.form(
                rx.vstack(
                    # Error message
                    rx.cond(
                        AuthState.error,
                        rx.box(
                            rx.text(
                                AuthState.error,
                                color=Color.ERROR,
                                text_align="center",
                                padding="0.5rem",
                                background_color=Color.SECONDARY,
                                border_radius="md",
                                width="100%"
                            ),
                            width="100%",
                            margin_bottom="1rem"
                        )
                    ),
                    # Username field
                    rx.hstack(
                        rx.icon(tag="user", padding_x="0.1rem", color=Color.PRIMARY_CONTENT, size=32),
                        rx.input(
                            placeholder="Username",
                            value=AuthState.username,
                            on_change=AuthState.set_username,
                            size="3",
                            width="100%",
                            focus_border_color=Color.PRIMARY,
                            _focus={"border_color": Color.PRIMARY},
                            _invalid={"border_color": Color.ERROR},
                            _disabled={"opacity": "0.6"},
                            _hover={"border_color": Color.PRIMARY},
                        ),
                        align_items="center",
                        width="100%"
                    ),
                    # Password field
                    rx.hstack(
                        rx.icon(tag="lock", padding_x="0.1rem", color=Color.PRIMARY_CONTENT, size=32),
                        rx.input(
                            placeholder="Contraseña",
                            type_=rx.cond(AuthState.show_password, "text", "password"),
                            value=AuthState.password,
                            on_change=AuthState.set_password,
                            size="3",
                            width="100%",
                            focus_border_color=Color.PRIMARY,
                            _focus={"border_color": Color.PRIMARY},
                            _invalid={"border_color": Color.ERROR},
                            _disabled={"opacity": "0.6"},
                            _hover={"border_color": Color.PRIMARY},
                        ),
                        rx.icon_button(
                            rx.icon(tag=rx.cond(AuthState.show_password, "eye-off", "eye"), color=Color.PRIMARY_CONTENT),
                            on_click=AuthState.toggle_show_password,
                            variant="ghost",
                            padding_x="0.5rem",
                            _hover={"background_color": Color.SECONDARY},
                        ),
                        align_items="center",
                        width="100%"
                    ),
                    # Remember me and forgot password
                    rx.hstack(
                        rx.checkbox(
                            "Recordarme",
                            on_change=AuthState.set_remember_me,
                            size="2",
                            color=Color.SECONDARY_CONTENT,
                            _hover={"color": Color.PRIMARY_CONTENT},
                        ),
                        rx.spacer(),
                        rx.link(
                            "¿Olvidaste tu contraseña?",
                            href="#",
                            size="2",
                            color=Color.ACCENT,
                            _hover={"color": Color.ACCENT_LIGHT},
                        ),
                        justify="between",
                        width="100%",
                    ),
                    # Login button
                    rx.button(
                        "Iniciar sesión",
                        type_="submit",
                        width="100%",
                        size="3",
                        is_loading=AuthState.is_loading,
                        is_disabled=rx.cond(
                            (AuthState.username == "") | (AuthState.password == ""),
                            True,
                            False,
                        ),
                        background_color=Color.PRIMARY,
                        color=Color.PRIMARY_CONTENT,
                        _hover={"background_color": Color.ACCENT_LIGHT},
                        _disabled={
                            "opacity": "0.6",
                            "cursor": "not-allowed"
                        },
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
            ),

            spacing="5",
            padding="2rem",
            max_width="450px",
            width="100%",
            bg=Color.BACKGROUND,
            border_radius="0.375rem",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        ),
        width="100%",
        height="100vh",
        padding="2rem",
        bg=Color.BACKGROUND,
    )
