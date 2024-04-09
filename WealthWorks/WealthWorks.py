"""Welcome to WealthWorks!"""
import reflex as rx

# Importing pages
from WealthWorks.pages.debtRepayment import debt_repayment
from WealthWorks.pages.goodToKnow import good_to_know
from WealthWorks.pages.budgetPlanner import planner
from WealthWorks.pages.news import news
from WealthWorks.pages.page404 import page404
from dotenv import load_dotenv
import os


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


load_dotenv()
umami_url = os.environ.get("UMAMI_URL")
website_id = os.environ.get("WEBSITE_ID")

app = rx.App(
    head_components=[
        rx.script(
            f"""
            (function() {{
                var script = document.createElement('script');
                script.async = true;
                script.src = "{umami_url}";
                script.setAttribute('data-website-id', '{website_id}');
                document.head.appendChild(script);
            }}) ();
            """
        ),
    ],
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        accentColor="blue",
        radius="large",
    ),
)
