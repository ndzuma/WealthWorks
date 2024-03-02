import reflex as rx


# Creator Information
creatorName: str = "Ndzuma Malate"
creatorEmail: str = "ndzumaxx@gmail.com"
creatorLinkedIn: str = "https://www.linkedin.com/in/ndzuma/"
creatorGitHub: str = "https://github.com/ndzuma"

# App Information
appTitle: str = "WealthWorks"
appFeedback: str = "https://codepulse.streamlit.app"


def header(page) -> rx.Component:
    if page == "/":
        budget_bg = "#4662D5"
        budget_color = "white"
        debt_bg = "-"
        debt_color = "-"
        news_bg = "-"
        news_color = "-"
        cookbook_bg = "-"
        cookbook_color = "-"
    elif page == "/debt-repayment":
        budget_bg = "-"
        budget_color = "-"
        debt_bg = "#4662D5"
        debt_color = "white"
        news_bg = "-"
        news_color = "-"
        cookbook_bg = "-"
        cookbook_color = "-"
    elif page == "/news":
        budget_bg = "-"
        budget_color = "-"
        debt_bg = "-"
        debt_color = "-"
        news_bg = "#4662D5"
        news_color = "white"
        cookbook_bg = "-"
        cookbook_color = "-"
    elif page == "/good_to_know":
        budget_bg = "-"
        budget_color = "-"
        debt_bg = "-"
        debt_color = "-"
        news_bg = "-"
        news_color = "-"
        cookbook_bg = "#4662D5"
        cookbook_color = "white"
    else:
        budget_bg = "-"
        budget_color = "-"
        debt_bg = "-"
        debt_color = "-"
        news_bg = "-"
        news_color = "-"
        cookbook_bg = "-"
        cookbook_color = "-"
    return rx.flex(
        rx.box(height="20px"),
        rx.heading(
            appTitle,
            font_family="Josefin Sans",
            size="9",
            align="center",
        ),
        rx.box(height="20px"),
        rx.vstack(
            rx.flex(
                rx.card(
                    rx.text(
                        rx.link("Budget Planner", href="/", color=budget_color),
                        size="3",
                        weight="medium",
                        align="center"
                    ),
                    width="100%",
                    height="3em",
                    bg_color=budget_bg,
                ),
                rx.card(
                    rx.text(
                        rx.link("Debt Repayment", href="/debt-repayment", color=debt_color),
                        size="3",
                        weight="medium",
                        align="center"
                    ),
                    width="100%",
                    height="3em",
                    bg_color = debt_bg,
                ),
                spacing="2",
                direction="row",
                width="100%"
            ),
            rx.flex(
                rx.card(
                    rx.text(
                        rx.link("Market News", href="/news", color=news_color),
                        size="3",
                        weight="medium",
                        align="center"
                    ),
                    width="100%",
                    height="3em",
                    bg_color=news_bg,
                ),
                rx.card(
                    rx.text(
                        rx.link("The Cookbook", href="/good_to_know", color=cookbook_color),
                        size="3",
                        weight="medium",
                        align="center"
                    ),
                    width="100%",
                    height="3em",
                    bg_color=cookbook_bg,
                ),
                spacing="2",
                direction="row",
                width="100%"
            )
        ),
        direction="column",
        width="100%"
    )


def footer() -> rx.Component:
    return rx.flex(
        rx.text("© 2024 ", creatorName),
        contact_me(),
        spacing="3",
        direction="row",
        justify="between",
        width="100%"
    )


def contact_me() -> rx.Component:
    # Should link to my portfolio
    return rx.dialog.root(
        rx.dialog.trigger(rx.link("Get in contact")),
        rx.dialog.content(
            rx.dialog.title("Hey! I'm ", creatorName),
            rx.dialog.description(
                "You can find on the following platforms:\n",
                rx.link("Email", href=f"mailto:{creatorEmail}?subject=Hello%20from%20a%20Visitor"),
                ", ", rx.link("LinkedIn", href=creatorLinkedIn),
                ", ", rx.link("GitHub", href=creatorGitHub)
            ),
            rx.dialog.description(rx.link("Send Feedback", href=appFeedback)),
            rx.dialog.close(
                rx.link("Close"),
            )
        ),
    )
