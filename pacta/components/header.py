import reflex as rx
from ..styles.styles import Color


def UserMenu():
    return rx.hstack(
        rx.menu.root(
            rx.menu.trigger(
                rx.avatar(
                    name="Usuario", 
                    size="3",
                    cursor="pointer",
                    fallback="US",
                ),
                # Ensure submenu opens on click
                trigger_action="click",
            ),
            rx.menu.content(
                rx.menu.item("Ajustes", on_click=rx.redirect("/ajustes")),
                rx.menu.separator(),
                rx.menu.item("Cerrar sesión", color=Color.ERROR, on_click=rx.redirect("/logout")),
                style={"min_width": "120px"},
            ),
        ),
        spacing="2",
        align_items="center",
    )

def Header():
    return rx.box(
        rx.hstack(
            # Remove spacer to align items to the left
            rx.button("Doc", as_="a", href="/doc", variant="ghost", _hover={"background_color": Color.ACCENT_LIGHT}, color=Color.WHITE),
            rx.button("Help", as_="a", href="/help", variant="ghost", _hover={"background_color": Color.ACCENT_LIGHT}, color=Color.WHITE),
            UserMenu(),
            spacing="4",
            align_items="center",
        ),
        as_="header",
        position="fixed",
        top="0",
        left="0",  # Align header fully left
        right="0",
        height="64px",
        width="100%",
        padding_x="1rem",
        background="linear-gradient(90deg, #468FAF 0%, #A9D6E5 100%)",  # Gradient blue to pastel blue
        color=Color.WHITE,  # White text and icons
        box_shadow="md",
        z_index=1000,
    )
