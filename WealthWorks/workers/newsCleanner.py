"""
NewsCleaner class is used to clean duplicate articles from the db.
"""
import postgrest.exceptions

import consoleStatements as Display
from typing import List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

import os


def clean_news() -> None:
    service = "NewsCleaner Service"

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

    # We clean the db by:
    # getting data -> removing duplicates(if any) -> deleting the duplicates -> Ordering the ids in the db
    data = fetchNews(supabase_url, supabase_api_key, service)
    cleaned_data, data_len = removeDuplicates(data, service)
    deleteArticles(url=supabase_url, key=supabase_api_key, service=service, old_articles=data, new_articles=cleaned_data)
    updateArticleIds(url=supabase_url, key=supabase_api_key, service=service, articles=cleaned_data)


def fetchNews(url: str, key: str, service: str) -> List[Dict[str, Any]]:
    """
    This function gets the news articles from the Supabase database
    :param url: Supabase URL
    :param key: Supabase API key
    :param service: Name of the service
    :return: List of news articles
    """
    # Create a Supabase client
    supabase: Client = create_client(url, key)
    response = supabase.table("WealthworksNews").select("*", count='exact').order("id", desc=False).execute()

    # Get the data from the response
    data = response.data

    return data


def removeDuplicates(data: List[Dict[str, Any]], service: str) -> (List[Dict[str, Any]], int):
    """
    This function removes duplicate articles from the list of articles and returns the cleaned list
    :param data: The list of articles
    :param service: Name of the service
    :return: A tuple containing the cleaned list of articles and the length of the cleaned list
    """
    # This function works by turning a list into a dictionary(HashMap) and then back into a list
    # This way, we can remove duplicates from the list

    # Remove articles with url duplicates
    test_data = {}
    for item in data:
        test_data[item["url"]] = item
    new_data = list(test_data.values())

    # Remove articles with title duplicates
    test_data = {}
    for item in new_data:
        test_data[item["title"]] = item
    new_data = list(test_data.values())

    old_len = len(data)
    new_len = len(new_data)
    Display.message(service, f"Removed {old_len - new_len} duplicate articles")

    return new_data, new_len


def deleteArticles(
        url: str,
        key: str,
        service: str,
        old_articles: List[Dict[str, Any]],
        new_articles: List[Dict[str, Any]]
) -> None:
    """
    This function deletes articles from the Supabase db that are not present in the new list of articles
    :param url: Supabase URL
    :param key: Supabase API key
    :param service: Name of the service
    :param old_articles: The old list of articles
    :param new_articles: The new list of articles
    :return: None
    """
    # Create a Supabase client
    supabase: Client = create_client(url, key)

    # List of ids of articles to be deleted
    ids = []

    if len(old_articles) > len(new_articles):
        # Find the ids of the articles to be deleted
        for article in old_articles:
            if article not in new_articles:
                ids.append(article['id'])

        # Bulk delete the articles
        try:
            supabase.table('WealthworksNews').delete().in_('id', ids).execute()
            Display.message(service, f"{len(ids)} articles deleted from db successfully")
        except postgrest.exceptions.APIError as e:
            Display.message(service, f"Error deleting articles: {e}")


def updateArticleIds(
        url: str,
        key: str,
        service: str,
        articles: List[Dict[str, Any]],
) -> None:
    """
    This function updates the ids of the articles in the db, if the ids are not in order
    :param url: Supabase URL
    :param key: Supabase API key
    :param service: Name of the service
    :param articles: The list of articles
    :return: None
    """
    # Create a Supabase client
    supabase: Client = create_client(url, key)

    # Number of articles updated
    updated_articles: int = 0

    # Update the id of each article to be in order
    for i, article in enumerate(articles):
        new_id = i + 1

        # Check if the id of the article is not already in order
        if article['id'] != new_id:
            try:
                # Update the id of the article
                supabase.table('WealthworksNews').update({'id': new_id}).eq('id', article['id']).execute()
                updated_articles += 1
                Display.message(service, f"Updated article with id {article['id']} to {new_id}")
            except postgrest.exceptions.APIError as e:
                # Display error message if the article could not be updated
                Display.message(service, f"Error updating article with id {article['id']}: {e}")

    Display.message(service, f"{updated_articles} articles updated successfully")


if __name__ == '__main__':
    clean_news()
