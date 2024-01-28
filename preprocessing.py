# This file


# USING REDDIT API
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import time
import requests
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
from TOP_CRYPTO import TOP_CRYPTO_LIST

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSWORD = os.getenv("PASSWORD")


def fetch_post(limit=500, after=None):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    pw = PASSWORD

    data = {"grant_type": "password", "username": "dowhatexcites_", "password": pw}

    headers = {"User-Agent": "MyBot/0.0.1"}

    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    TOKEN = res.json()["access_token"]  # access token!
    headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    # requests.get("https://oauth.reddit.com/api/v1/me", headers=headers).json()

    params = {"limit": limit, "after": after}
    res = requests.get(
        "https://oauth.reddit.com/r/CryptoCurrency/hot", headers=headers, params=params
    )

    # posts = []
    # while len(posts) < 200:
    #     # Make a request to the Pushshift API
    #     response = requests.get(
    #         "https://oauth.reddit.com/r/CryptoCurrency/hot",
    #         headers=headers,
    #         params=params,
    #     )
    #     # Check if the request was successful (status code 200)
    #     if response.status_code == 50:
    #         data = response.json()["data"]["children"]
    #         if not data:
    #             # No more posts available
    #             break

    #         posts.extend(data)
    #         print(f"Downloaded {len(posts)} posts")

    #         # Set the timestamp for the next request to the created_utc of the last post
    #         # params["before"] = data[-1]["created_utc"]
    #     else:
    #         # Handle failed request
    #         print(f"Request failed with status code {response.status_code}")
    #         break

    #     # Add a delay to avoid hitting API rate limits
    #     time.sleep(1)

    # print(posts)
    df = pd.DataFrame()
    data = []
    # Loop through each post retrieved from GET request
    for post in res.json()["data"]["children"]:
        # If the body of a post is empty, then make the body the title of the post
        idx = "selftext"
        if post["data"]["selftext"] == "":
            idx = "title"

        created_utc = post["data"]["created_utc"]
        created_time = datetime.utcfromtimestamp(created_utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        data.append(
            {
                "subreddit": post["data"]["subreddit"],
                "title": post["data"]["title"],
                "selftext": post["data"][idx],
                "upvote_ratio": post["data"]["upvote_ratio"],
                "ups": post["data"]["ups"],
                "downs": post["data"]["downs"],
                "score": post["data"]["score"],
                "created_utc": created_utc,
                "created_time": created_time,
            }
        )

    for d in data:  # filter all posts that have a upvote ratio < 0.5
        if not validate_post(d):
            data.remove(d)
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    # print(df)

    return data


# ------------------------------------------Preprocessing------------------------------------------
def validate_post(post):
    return post["upvote_ratio"] > 0.5


# 1. Converts the text to lowercase.
# 2. Removes HTML tags using regular expressions.
# 3. Removes non-alphabetic characters using regular expressions.
# 4. Tokenizes the text into words.
# 5. Removes stop words using NLTK's English stop words.
# 6. Applies stemming using the Porter stemming algorithm.
# 7. Joins the processed words back into a string.

# Download NLTK resources
# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.downloader.download("vader_lexicon")


def preprocess_text_list(post_list):
    appeared_coin = []
    for post in post_list:
        appeared_words = [
            word
            for word in TOP_CRYPTO_LIST
            if re.search(
                rf"\b{re.escape(word)}\b",
                post["selftext"] + post["title"],
                flags=re.IGNORECASE,
            )
        ]
        appeared_coin.append(appeared_words)

    # Add a new key "appeared_words" to each post dictionary
    for post, appeared_words in zip(post_list, appeared_coin):
        post["coins"] = appeared_words

    df = pd.DataFrame(post_list)
    df["ID"] = range(len(df))
    df.insert(0, "ID", df.pop("ID"))

    print(len(df))
    file_path = "posts.csv"
    df.to_csv(file_path, index=False)

    # I'm not sure the following processes are actually useful????????
    # processed_texts = []
    # for post in post_list:
    #     text = post["selftext"]
    #     text = text.lower()
    #     # Remove HTML tags using regular expressions
    #     text = re.sub(r"<[^>]+>", "", text)

    #     # Remove non-alphabetic characters using regular expressions
    #     text = re.sub(r"[^a-z\s]", "", text)

    #     # Tokenize the text into words
    #     words = text.split()

    #     # Remove stop words using NLTK's English stop words
    #     stop_words = set(stopwords.words("english"))
    #     words = [word for word in words if word not in stop_words]

    #     # Apply stemming using the Porter stemming algorithm (removing the commoner morphological and inflexional endings from words in English)
    #     stemmer = PorterStemmer()
    #     words = [stemmer.stem(word) for word in words]

    #     # # Join the processed words back into a string
    #     processed_text = " ".join(words)

    #     # formatted_string = "|".join([f"{name}|{symbol}" for name, symbol in TOP_CRYPTO])
    #     # crypto_identifier = find_single_crypto_identifier(text, formatted_string)
    #     # print("crypto_identifier: ", crypto_identifier)

    #     processed_texts.append(processed_text)
    #     post["selftext"] = processed_text


if __name__ == "__main__":
    text_list = fetch_post(limit=500)
    preprocessed_list = preprocess_text_list(
        text_list
    )  # format: (processed_text, [identifiers])

    # print("preprocessed_posts: ", preprocessed_posts)
