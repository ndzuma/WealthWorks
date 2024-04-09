<h1 align="center">WealthWorks</h1>

A place to get your personal finances in order. You can visit the live version of the app [here](https://wealthworks.reflex.run/).

![Budget planner _ WealthWorks.jpeg](assets%2FBudget%20planner%20_%20WealthWorks.jpeg)

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
    ```
2. Navigate to the project directory:

   ```bash
   cd WealthWorks
   ```
3. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:

      ```bash
      venv\Scripts\activate
      ```
   - On macOS and Linux:

      ```bash
       source venv/bin/activate
       ```
5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
6. In the 'workers' folder, create a `.env` file and add the following environment variables:

   ```bash
   MARKETAUX_API_KEY=your_market_aux_api_key
   SUPABASE_API_KEY=your_supabase_api_key
   SUPABASE_URL=your_supabase_url
   ```
7. Initialise reflex:

   ```bash
   reflex init
   ```
   if you encounter an error, try one of the following command:

   ```bash
   python -m reflex init
   python3 -m reflex init
    ```
8. Run the app:

   ```bash
   reflex run
   ```
   if you encounter an error, try one of the following command:

   ```bash
   python -m reflex run
   python3 -m reflex run
    ```
9. Open your browser and navigate to `http://localhost:3000/` to view the app.
