"""Welcome to WealthWorks!"""
import reflex as rx

from WealthWorks.pages.debtRepayment import debt_repayment
from WealthWorks.pages.goodToKnow import good_to_know
from WealthWorks.pages.budgetPlanner import planner
from WealthWorks.pages.news import news
from WealthWorks.pages.page404 import page404


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
    route="/news",
    title="Market news | WealthWorks"
)
def market_news() -> rx.Component:
    return news()


@rx.page(
    route="/good_to_know",
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
    head_components=[
        rx.script(
            """
            (function() {
                var script = document.createElement('script');
                script.async = true;
                script.src = "https://umami.ndzuma.pro/script.js";
                script.setAttribute('data-website-id', 'b9493033-fdcb-451d-addc-7c8d17e6e64f');
                document.head.appendChild(script);
            }) ();
            """
        ),
    ],
    theme=rx.theme(
        appearance="dark",
        accentColor="blue",
        radius="large",
    ),
)
