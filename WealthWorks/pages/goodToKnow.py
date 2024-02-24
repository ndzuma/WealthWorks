import reflex as rx

from WealthWorks.components import basic


# Main section
def good_to_know() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/good-to-know"),
            rx.chakra.divider(border_color="lightgrey"),
            basic.footer(),
            rx.box(min_height="10px"),
            direction="column",
            max_width="50em",
            spacing="5",
        ),
        rx.spacer(min_width="10px"),
        justify="center",
        direction="row",
        height="100vh",
    )
