"""Welcome to WealthWorks!"""
import reflex as rx

from WealthWorks.pages.debtRepayment import debt_repayment
from WealthWorks.pages.budgetPlanner import planner
from WealthWorks.pages.page404 import page404
from WealthWorks.pages.goodToKnow import good_to_know


# All pages
@rx.page(
    route="/",
    title="Budget planner | WealthWorks"
)
def index() -> rx.Component:
    return planner()


@rx.page(
    route="/debt-repayment",
    title="Debt repayment planner | WealthWorks"
)
def debt() -> rx.Component:
    return debt_repayment()

@rx.page(
    route="/good-to-know",
    title="Good to Know | WealthWorks"
)
def debt() -> rx.Component:
    return good_to_know()


@rx.page(
    route="/404",
    title="Page Not Found | WealthWorks"
)
def not_found() -> rx.Component:
    return page404()


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
    )

)
