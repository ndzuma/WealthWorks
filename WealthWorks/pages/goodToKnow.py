import reflex as rx
import os

from typing import List, Dict, Optional
from WealthWorks.components import basic
from WealthWorks.components.extra import linear_gradient
from WealthWorks.components.extra import hex_to_rgba


class CookbookType(rx.Base):
    title: str
    markdown: str
    author: str


class CookbookState(rx.State):
    articles: List[CookbookType]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.articles = self.getArticles()

    def getArticles(self) -> List[CookbookType]:
        """
        This function gets the articles from the docs directory
        :return: A list of articles
        """
        articles = []
        current_dir = os.getcwd() + "/WealthWorks/docs"
        article_dir = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        for i in article_dir:
            md = self.md_to_str(current_dir + "/" + i)
            articles.append(CookbookType(
                title=i.replace(".md", ""),
                markdown=md,
                author="WealthWorks"
            ))
        return articles

    @staticmethod
    def md_to_str(md_file_path) -> str:
        """
        This function converts markdown to string
        :param md_file_path: The path to the markdown file
        :return: The markdown content as a string
        """
        print(md_file_path)
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        return markdown_content


def info(headline, color1: str, trans1: float, color2: str, trans2: float, content) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.link(
                rx.chakra.card(
                    rx.flex(
                        rx.text(headline, size="5", as_="b"),
                        rx.chakra.icon(tag="arrow_forward", boxSize="1.3em"),
                        direction="row",
                        align="center",
                        justify="between",
                        height="100%",
                    ),
                    height="100px",
                    bgGradient=linear_gradient(
                        hex_to_rgba(hex_color=color1, transparency=trans1),
                        hex_to_rgba(hex_color=color2, transparency=trans2)
                    ),
                    border_radius="8",
                )
            )
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Close",
                        variant="soft",
                        color_scheme="gray",
                        width="100%",
                    ),
                ),
            ),
            rx.flex(
                rx.markdown(content.markdown),
                direction="column",
                spacing="2",
                color="white",
            ),
            width="100%",
            size="4",
        )
    )


def info_block(item) -> rx.Component:
    return info(item.title, "#2F53D5", 1, "#50D52F", 0.3, item)


def info_blocks() -> rx.Component:
    """
    This function returns a list of article cards
    """
    return rx.flex(
        rx.foreach(
            CookbookState.articles,
            info_block

        ),
        spacing="3",
        width="100%",
        direction="column"
    )


# Main section
def good_to_know() -> rx.Component:
    return rx.flex(
        rx.theme_panel(default_open=False),
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/good-to-know"),
            info_blocks(),
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
