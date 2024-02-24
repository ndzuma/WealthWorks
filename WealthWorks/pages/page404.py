import reflex as rx

contents = f"""
# Page Not Found

The page at `{rx.State.router.page.raw_path}` doesn't exist.
"""


def page404():
    return rx.center(
        rx.vstack(
            rx.markdown(contents),
            rx.spacer(),
        ),
        height="80vh",
        width="100%",
    )