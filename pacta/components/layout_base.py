import reflex as rx
from .sidebar import Sidebar
from .header import Header
from ..styles.styles import Color


def LayoutBase(children):
    return rx.box(
        Sidebar(),
        Header(),
        rx.box(
            children,
            as_="main",
            margin_left="220px",
            margin_top="64px",
            padding="2rem",
            height="calc(100vh - 64px)",
            overflow_y="auto",
            background_color=Color.BACKGROUND,
        ),
        width="100vw",
        height="100vh",
        background_color=Color.BACKGROUND,
    )
