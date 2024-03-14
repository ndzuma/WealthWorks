import reflex as rx

from WealthWorks.components import basic
from WealthWorks.components.extra import linear_gradient
from WealthWorks.components.extra import hex_to_rgba


def info_block(headline, color1: str, trans1: float, color2: str, trans2: float) -> rx.Component:
    return rx.link(
        rx.chakra.card(
            rx.flex(
                rx.text(headline, size="5", as_="b"),
                rx.chakra.icon(tag="arrow_forward", boxSize="1.3em"),
                direction="row",
                align="center",
                justify="between",
                height="100%",
            ),
            height="100px",
            bgGradient=linear_gradient(
                hex_to_rgba(hex_color=color1, transparency=trans1),
                hex_to_rgba(hex_color=color2, transparency=trans2)
            ),
            border_radius="8",
        )
    )


def info_blocks() -> rx.Component:
    return rx.flex(
        info_block("Personal finance starter guide", "#2F53D5", 1, "#50D52F", 0.3),
        info_block("The Budget cookbook", "#631243", 1, "#6427B3", 0.3),
        info_block("The Investing cookbook", "#6427B3", 1, "#998746", 0.3),
        info_block("Your friendly emergency fund", "#2F53D5", 1, "#50D52F", 0.3),
        spacing="3",
        width="100%",
        direction="column"
    )


# Main section
def good_to_know() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/good-to-know"),
            info_blocks(),
            rx.chakra.divider(border_color="lightgrey"),
            basic.footer(),
            rx.box(min_height="10px"),
            direction="column",
            width="100%",
            max_width="50em",
            spacing="5",
        ),
        rx.spacer(min_width="10px"),
        justify="center",
        direction="row",
        width="100vw",
        height="100vh",
    )
