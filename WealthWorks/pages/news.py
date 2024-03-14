import reflex as rx

from WealthWorks.components import basic
from WealthWorks.components import extra


def news_block() -> rx.Component:
    return rx.chakra.card(
        rx.link(
            rx.flex(
                rx.chakra.heading("CNBC", size="sm"),
                rx.chakra.text(
                    "Chinese leaders to hold annual 'Two Sessions' meeting as debate about bazooka-like stimulus swirls"
                ),
                direction="column",
                spacing="2"
            ),
            color="white"
        ),
        border_radius="8",
        border="1px solid #303237",
        bg="#18191C",
        size="md"
    )


def news_blocks() -> rx.Component:
    return rx.flex(
        news_block(),
        news_block(),
        news_block(),
        direction="column",
        spacing="3",
    )


# Main section
def news() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/news"),
            news_blocks(),
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
