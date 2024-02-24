import reflex as rx


def coming_soon() -> rx.Component:
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
