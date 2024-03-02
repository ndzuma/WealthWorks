import reflex as rx

from WealthWorks.components import basic
from WealthWorks.components import extra


# State
class DebtState(rx.State):
    name: str


# Main section
def debt_repayment() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/debt-repayment"),
            extra.coming_soon(),
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
