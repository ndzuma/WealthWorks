# WealthWorks
A place to get your personal finances in order. You can visit the live version of the app [here](https://wealthworks.reflex.run/).

## Overview

WealthWorks is built entirely using the Reflex Python library, PostgreSQL with Supabase, and MarketAux for fetching market news. The application provides various features:

- **Budget Management:** Users can create and manage their budgets.
- **Debt Repayment Calculator:** Helps users calculate how long it will take to pay off their debts and the minimum monthly payments required.
- **Market News:** Provides users with the latest news from the financial markets.
- **Personal Finance Learning:** Offers educational resources on personal finance through the "The Cookbook" page.

## Adaptation

You can adapt the app to different databases by modifying the modules in the `workers` folder, particularly `newsCollector.py`, `newsFetcher.py`, and `newsCleanner.py`. Additionally, the content displayed on the "The Cookbook" page can be updated by modifying the Markdown files in the `docs` folder.

## Environment Variables

Ensure that the following environment variables are set up:

- `MARKETAUX_API_KEY`: API key for MarketAux.
- `SUPABASE_API_KEY`: API key for Supabase.
- `SUPABASE_URL`: URL for Supabase.

## Requirements

To run the web app, make sure you have the following dependencies installed:

- reflex==0.4.4
- reportlab==4.1.0
- wheel==0.42.0
- python-dotenv~=1.0.1
- requests~=2.31.0
- supabase~=2.4.0
- markdown2~=2.4.13
- postgrest~=0.16.1

## Usage

To run the WealthWorks web app locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ndzuma/WealthWorks.git

