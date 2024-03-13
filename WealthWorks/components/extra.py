from typing import List

import reflex as rx


def coming_soon() -> rx.Component:
    """
    Returns a "coming soon" card.
    :return:
    """
    return rx.flex(
        rx.card(
            rx.box(height="40%"),
            rx.text("Under construction!", size="6", weight="medium", align="center", height="20%"),
            rx.box(height="40%"),
            height="50vh",
            width="100%",
        ),
        width="100%"
    )


def linear_gradient(*colors: str) -> str:
    """
    Returns a linear gradient string for use in CSS.
    :param colors:
    :return: str
    """
    return f"linear(to-r, {', '.join(colors)})"


def hex_to_rgb(hex_color: str) -> list[int]:
    """
    Convert a hex color to RGB
    :param hex_color: hex color string
    :return: rgb list
    """
    # Remove the '#' character if present
    hex_color = hex_color.lstrip('#')

    # Convert hex color to RGB
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    return [red, green, blue]


def hex_to_rgba(hex_color: str, transparency: float) -> str:
    """
    Convert a hex color to an RGBA string
    :param hex_color: str
    :param transparency: float
    :return: str
    """
    rgb = hex_to_rgb(hex_color)
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {transparency})"
