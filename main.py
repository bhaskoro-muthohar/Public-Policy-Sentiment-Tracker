import asyncio
from twscrape import API, gather
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import json

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
email = os.getenv('EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')

# search_terms = ["#qris", "#mbanking"]
location_params = "-2.7085863647685455,118.05612276107703,2700km"

def load_accounts():
    accounts = []
    i = 1
    while True:
        username = os.getenv(f'USERNAME{i}')
        password = os.getenv(f'PASSWORD{i}')
        email = os.getenv(f'EMAIL{i}')
        email_password = os.getenv(f'EMAIL_PASSWORD{i}')
        if not username or not password or not email or not email_password:
            break
        accounts.append((username, password, email, email_password))
        i += 1
    return accounts

def load_search_terms(filename):
    with open(filename, 'r') as file:
        terms = file.readlines()
    search_terms = []
    for term in terms:
        items = term.strip().split(',')
        first_term = items[0].split('. ')[-1].strip()
        search_terms.append(first_term)
        if len(items) > 1:
            search_terms.append(items[1].strip())
    return search_terms

def save_to_json(tweets, filename):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(tweets, file, ensure_ascii=False, indent=4)

async def main():
    api = API()
    accounts = load_accounts()

    # Add all accounts to the pool
    for username, password, email, email_password in accounts:
        await api.pool.add_account(username, password, email, email_password)
    
    await api.pool.login_all()

    search_terms = load_search_terms("search_terms.txt")
    start_date = "2021-01-01"
    end_date = "2024-06-30"
    all_tweets = []
    limit = 0
    
    # Iterate over each search term and perform a search
    for term in search_terms:
        print(f"Searching for: {term} in location: {location_params}")
        
        # Include date range in the search query
        search_query = f"{term} geocode:{location_params} since:{start_date} until:{end_date}"
        print(f"Search Query: {search_query}")
        
        if limit > 0:
            search_generator = api.search(search_query, limit=limit)
        else:
            search_generator = api.search(search_query)

        async for tweet in search_generator:
            tweet_data = {
                'tweet_id': tweet.id,
                'id_str': tweet.id_str,
                'url': tweet.url,
                'date': tweet.date.isoformat() if isinstance(tweet.date, datetime) else tweet.date,
                'user': {
                    'id': tweet.user.id,
                    'id_str': tweet.user.id_str,
                    'url': tweet.user.url,
                    'username': tweet.user.username,
                    'displayname': tweet.user.displayname,
                    'rawDescription': tweet.user.rawDescription,
                    'created': tweet.user.created.isoformat() if isinstance(tweet.user.created, datetime) else tweet.user.created,
                    'followersCount': tweet.user.followersCount,
                    'friendsCount': tweet.user.friendsCount,
                    'statusesCount': tweet.user.statusesCount,
                    'favouritesCount': tweet.user.favouritesCount,
                    'listedCount': tweet.user.listedCount,
                    'mediaCount': tweet.user.mediaCount,
                    'location': tweet.user.location,
                    'protected': tweet.user.protected,
                    'verified': tweet.user.verified,
                },
                'lang': tweet.lang,
                'content': tweet.rawContent,
                'replyCount': tweet.replyCount,
                'retweetCount': tweet.retweetCount,
                'likeCount': tweet.likeCount,
                'quoteCount': tweet.quoteCount,
                'hashtags': tweet.hashtags
            }
            all_tweets.append(tweet_data)

        save_to_json(all_tweets, 'tweets.json')

        print("Scrapping Finished!")

if __name__ == "__main__":
    asyncio.run(main())
