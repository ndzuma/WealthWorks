"""
News Fetcher Service:
This module contains the functions to fetch the news articles from the Supabase database
"""
from WealthWorks.workers import consoleStatements as Display
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

import os


def FetchNews() -> List:
    """
    This function gets the news articles from the database and returns them and a dictionary
    containing the page number as the key and the id of the first news article on that page as the value
    :return: A list of dictionaries containing the news articles and a dictionary containing the page number as the key and the id of the first news article on that page as the value
    """
    service = "News Fetcher Service"

    # Displaying start confirmation
    Display.start(service)

    # Loading environment variables
    load_dotenv()
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_api_key = os.environ.get("SUPABASE_API_KEY")

    # Checking if API keys were provided
    if supabase_url is None:
        Display.message(service, "Supabase URL is not set")
        Display.completed(service)
        raise SystemExit(0)
    if supabase_api_key is None:
        Display.message(service, "Supabase API Key is not set")
        Display.completed(service)
        raise SystemExit(0)

    # Get the news articles from the Supabase database
    news = getNews(url=supabase_url, key=supabase_api_key)

    # Get the page number and the id of the first news article on that page
    numArticles = 5
    numPages = findTotalPages(url=supabase_url, key=supabase_api_key, articles_per_page=numArticles)
    pageIdIndex = getPagesId(number_of_pages=numPages[0], first_id=numPages[1], articles_per_page=numArticles)

    # Display completion of service
    Display.completed(service)

    return [news, pageIdIndex]


def getNews(
        url: str,
        key: str,
) -> List[Dict[str, Any]]:
    """
    This function gets the news articles from the Supabase database

    You can get the API key and documentation from the Supabase website: https://supabase.com/

    :param url: The URL for the Supabase API
    :param key: The API key for the Supabase API
    :return: The list of dictionaries containing the news articles
    """
    supabase: Client = create_client(url, key)
    response = supabase.table("WealthworksNews").select("*", count='exact').order("id", desc=True).execute()
    data = response.data

    return data


def getPagesId(
    number_of_pages: int,
    first_id: int,
    articles_per_page: Optional[int] = 5
) -> Dict[int, int]:
    """
    This function returns the id of the first news article on each page

    Example return: {1: 24, 2: 19, 3: 14} where the key value pairs are {page: first_id}

    :param number_of_pages: The total number of pages possible
    :param first_id: The id of the first news article on the first page or in other words the newest news article
    :param articles_per_page: The number of articles per page
    :return: A dictionary containing the page number as the key and the id of the first news article on that page as the value
    """
    pages = {}

    # Looping through the pages and finding the id of the first news article on each page
    for i in range(1, number_of_pages + 1):
        pages[i] = first_id
        first_id -= articles_per_page

    return pages


def findTotalPages(
    url: str,
    key: str,
    articles_per_page: Optional[int] = 5
) -> List[int]:
    """
    This function finds the total number of pages possible

    :param url: The URL for the Supabase API
    :param key: The API key for the Supabase API
    :param articles_per_page: The number of articles per page
    :return: The total number of pages possible
    """
    supabase: Client = create_client(url, key)

    # Finding the first and last id of the news article
    #
    # There is a simpler way to do this using a simple query, but supabase doesn't support it, yet
    # We would have done something like this:
    # sql = "SELECT COUNT(*) FROM WealthworksNews;"
    # response = supabase.query(sql).execute()
    newest_article = supabase.table("WealthworksNews").select("*").limit(1).order("id", desc=True).single().execute()
    oldest_article = supabase.table("WealthworksNews").select("*").limit(1).order("id", desc=False).single().execute()

    # Finding the total number of articles in the database
    n_articles = newest_article.data['id'] - (oldest_article.data['id'] - 1)

    # Finding the total number of pages possible
    n_pages = n_articles // articles_per_page
    if n_articles % articles_per_page != 0:
        n_pages += 1

    return [n_pages, newest_article.data['id']]
