"""
News Collector Service:
This service collects news articles from the MarketAux API and sends them to the Supabase database
"""
import consoleStatements as Display
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

import requests
import os


def main():
    # Displaying start confirmation
    this_service = "News Collector Service"
    Display.start(this_service)

    # Loading environment variables
    load_dotenv()
    marketaux_key = os.getenv("MARKETAUX_API_KEY")
    supabase_key = os.getenv("SUPABASE_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")

    # Checking if API keys were provided
    if marketaux_key is None:
        Display.message(this_service, " MarketAux API Key is not set")
        Display.completed(this_service)
        raise SystemExit(0)  # Kill the program
    if supabase_url is None:
        Display.message(this_service, " Supabase URL is not set")
        Display.completed(this_service)
        raise SystemExit(0)  # Kill the program
    if supabase_key is None:
        Display.message(this_service, " Supabase API Key is not set")
        Display.completed(this_service)
        raise SystemExit(0)  # Kill the program

    # Get the news articles from marketaux
    news_articles = getNews(service=this_service, key=marketaux_key)

    # Send the news to the supabase database
    sendToDb(service=this_service, key=supabase_key, url=supabase_url, articles=news_articles)

    # Correct the size of the database
    correctDbSize(key=supabase_key, url=supabase_url)

    # Display completion of service
    Display.completed(this_service)


def getNews(
    key: str,
    service: Optional[str] = "News fetcher service"
) -> List[Dict[str, Any]]:
    """
    This function gets the news articles from the MarketAux API

    You can get the API key and documentation from the MarketAux website: https://www.marketaux.com/

    :param key: The API key for the MarketAux API
    :param service: The name of the service you are calling this program
    :return: A list of dictionaries containing the news articles
    """
    # Creating an array to store the articles
    articles = []
    # Generating 3 requests to the API, each returning 3 news stories (So 9 stories in total)
    for n in range(1, 4):
        r = requests.get(
            f"https://api.marketaux.com/v1/news/all?industries=Financial,Technology,Real Estate&filter_entities=true&language=en&page={n}&api_token={key}")
        status_code = r.status_code
        # Request error handling
        if status_code != 200:
            if status_code == 400:
                Display.message(service, "Parameter issues")
            elif status_code == 401:
                Display.message(service, "No Api token")
            elif status_code == 402:
                Display.message(service, "Usage limit reached")
            elif status_code == 403:
                Display.message(service, "You too broke, UP your subscription")
            elif status_code == 429:
                Display.message(service, "Too many requests in the last minute")
            else:
                Display.message(service, f"Error - check the error docs for status code {status_code}")
        else:
            data = r.json()
            data = data["data"]

            for i in range(len(data)):
                # Extracting information from the request
                title = data[i]["title"]
                description = data[i]["description"]
                url = data[i]["url"]
                image = data[i]["image_url"]
                source = data[i]["source"]
                company_name = data[i]["entities"][0]["name"]
                symbol = data[i]["entities"][0]["symbol"]
                equity_type = data[i]["entities"][0]["type"]
                country = data[i]["entities"][0]["country"]
                sentiment_score = data[i]["entities"][0]["sentiment_score"]

                # Add the article info to the array
                articles.append({
                    "title": title,
                    "description": description,
                    "url": url,
                    "image": image,
                    "source": source,
                    "name": company_name,
                    "symbol": symbol,
                    "equity_type": equity_type,
                    "country": country,
                    "sentiment_score": sentiment_score
                })

            # Displaying confirmation to terminal
            Display.message(service, "Articles successfully acquired")

    return articles


def sendToDb(
    key: str,
    url: str,
    articles: List[Dict[str, Any]],
    service: Optional[str] = "Supabase insert service"
):
    """
    This function sends the news articles to the Supabase database

    You can get the API key and documentation from the Supabase website: https://supabase.com/

    :param key: The API key for the Supabase API
    :param url: The URL for the Supabase database
    :param articles: The list of dictionaries containing the news articles
    :param service: The name of the service you are calling this program
    """
    supabase: Client = create_client(url, key)

    # Inserting the articles into the database
    supabase.table("WealthworksNews").insert(articles).execute()

    # Displaying confirmation to terminal
    Display.message(service, "Articles inserted successfully")


def correctDbSize(
    key: str,
    url: str,
    max_size: Optional[int] = 1000,
    service: Optional[str] = "DB size correction service"
):
    """
    This function corrects the size of the database by removing the oldest news articles, for size optimization

    :param key: The API key for the Supabase API
    :param url: The URL for the Supabase database
    :param max_size: The maximum size of the database
    :param service: The name of the service you are calling this program
    """
    # Displaying start confirmation
    Display.start(service)

    supabase: Client = create_client(url, key)
    # Getting the number of news articles in the database
    response = supabase.table("WealthworksNews").select("id", count='exact').execute()
    db_size = response.count

    # If the number of news articles is greater than 1000, remove the oldest articles
    if db_size > max_size:
        # Displaying message to terminal
        Display.message(service, "Size is greater than max size")

        # Getting the oldest news articles
        response = supabase.table("WealthworksNews").select("id").limit(db_size - max_size).order("id", desc=False).execute()
        data = response.data
        ids = [i["id"] for i in data]

        # Removing the oldest news articles
        supabase.table("WealthworksNews").delete().in_("id", ids).execute()

        # Displaying confirmation to terminal
        Display.completed(service)
    else:
        # Displaying message to terminal
        Display.message(service, "Size is less than max size")

        # Displaying completion of service
        Display.completed(service)


if __name__ == "__main__":
    main()
