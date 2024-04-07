import reflex as rx

from datetime import datetime
from typing import List, Dict, Optional
from WealthWorks.components import basic
from WealthWorks.workers.newsFetcher import FetchNews


class NewsType(rx.Base):
    title: str
    description: str
    date: str
    url: str
    source: str
    name: str
    symbol: str
    sentiment_score: float
    sentiment_color: str
    sentiment_text: str
    equity_type: str


class NewsState(rx.State):
    articles: List[NewsType]
    pageIdIndex: Dict[int, int]
    page: int
    previous_page: bool
    next_page: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.articles = []
        self.pageIdIndex = {}
        self.page = 1
        self.previous_page = True
        self.next_page = True
        self.set_articles()

    def set_articles(self, page: Optional[int] = 1):
        fetched_news = FetchNews()
        articles = fetched_news[0]
        for i in articles:
            sentiment_text, sentiment_color = self.calculate_sentiment_score(i["sentiment_score"])
            self.articles.append(NewsType(
                title=i["title"],
                description=self.truncate_description(i["description"]),
                date=self.date(i["created_at"]),
                url=i["url"],
                source=i["source"],
                name=i["name"],
                symbol=i["symbol"],
                sentiment_score=i["sentiment_score"],
                sentiment_color=sentiment_color,
                sentiment_text=sentiment_text,
                equity_type=i["equity_type"]
            ))
        self.pageIdIndex = fetched_news[1]

    @staticmethod
    def date(date):
        dt_object = datetime.fromisoformat(date)
        date = dt_object.strftime("%d-%m-%y")
        return date

    @staticmethod
    def truncate_description(description: str):
        """
        This function truncates the description of the news article to 50 characters
        :param description: The description of the news article
        :return: The truncated description
        """
        return description[:100] + "..." if len(description) > 100 else description

    @staticmethod
    def calculate_sentiment_score(sentiment_score: float):
        """
        This function calculates the sentiment score of the news article
        :param sentiment_score: The sentiment score of the news article
        :return: The sentiment score of the news article
        """
        if sentiment_score == 0:
            return "Neutral sentiment", "amber"
        elif sentiment_score > 0:
            return "Positive sentiment", "green"
        else:
            return "Negative sentiment", "red"


def news_block(item) -> rx.Component:
    return rx.chakra.card(
        rx.flex(
            rx.link(rx.chakra.heading(item.title, size="md"), href=item.url, is_external=True, color="white"),
            rx.link(rx.chakra.text(item.description), href=item.url, is_external=True, color="white"),
            rx.flex(
                rx.badge(item.sentiment_text, variant="soft", color_scheme=item.sentiment_color),
                rx.cond(
                    item.equity_type == "cryptocurrency",
                    rx.badge(item.equity_type, variant="soft", color_scheme="gold"),
                ),
                rx.badge(item.source, variant="soft"),
                rx.badge(item.name, variant="soft"),
                rx.badge(item.symbol, variant="soft"),
                direction="row",
                spacing="2",
                wrap="wrap",
            ),
            direction="column",
            spacing="2",
            color="white",
        ),
        border_radius="8",
        border="1px solid #303237",
        bg="#18191C",
        size="md"
    )


def news_blocks() -> rx.Component:
    return rx.flex(
        rx.foreach(
            NewsState.articles,
            news_block
        ),
        direction="column",
        spacing="3",
    )


def news_pagination() -> rx.Component:
    return rx.flex(
        rx.chakra.button_group(
            rx.chakra.button("Previous", is_disabled=NewsState.previous_page),
            rx.chakra.button("Next", is_disabled=NewsState.next_page),
        ),
        justify="center",
    )


# Main section
def news() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/news"),
            news_blocks(),
            # news_pagination(), # Pagination is not implemented yet
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
