from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re


# ------------------------------Sentiment analysis-------------------------------------
# TODO: find a better sentiment analysis library
def sentiment_analysis(preprocessed_posts):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for index, post in enumerate(preprocessed_posts):
        sentiment_score = analyzer.polarity_scores(post[0])
        sentiment_scores.append((index, sentiment_score))
        print(f"{index}. Sentiment Score: {sentiment_score}\nPost: {post[0]}\n")

    return sentiment_scores


# ---------------------------------Generating recommendation--------------------------------
def generate_recommendation(posts, sentiment_scores):
    print("\n")
    print("\n")
    recommendations = []
    # print("posts length: ", len(posts))
    # print("sentiment_scores length: ", len(sentiment_scores))
    # return

    for post, sentiment in zip(posts, sentiment_scores):
        if sentiment["compound"] >= 0:
            recommendations.append(
                {
                    "title": post,
                    "sentiment_score": sentiment["compound"],
                }
            )

    # Sort recommendations by sentiment score
    recommendations.sort(key=lambda x: x["sentiment_score"], reverse=True)

    return recommendations


def find_single_crypto_identifier(text, formatted_string):
    identifier_pattern = re.compile(rf"\b({formatted_string})\b", re.IGNORECASE)

    identifier = identifier_pattern.findall(text)
    symbols = [crypto[0] for crypto in identifier]
    if identifier:
        return symbols

    return None


# -----------------------------getting crypto names and tickers (run only occasionally, if not ever)-------------------------------
# def get_top_cryptos_names_and_symbols(limit=100):
#     url = f"https://api.coingecko.com/api/v3/coins/markets"

#     params = {
#         "vs_currency": "usd",
#         "order": "market_cap_desc",
#         "per_page": limit,
#         "page": 1,
#         "sparkline": False,
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     if isinstance(data, list):
#         names_and_symbols = [(crypto["name"], crypto["symbol"]) for crypto in data]
#         print("NAMES AND SYMBOLS: ", names_and_symbols)
#         return names_and_symbols
#     else:
#         print("Error fetching data from the coingecko API.")
#         return []


# -------------------------------------Identifying the tickers--------------------------------------
def find_cryptocurrency_identifiers(text_list, formatted_string):
    identifier_pattern = re.compile(rf"\b({formatted_string})\b", re.IGNORECASE)

    identifiers_found = []
    for text in text_list:
        identifiers = identifier_pattern.findall(text)
        if identifiers:
            identifiers_found.extend(identifiers[0])

    unique_identifiers = list(set(identifiers_found))

    return unique_identifiers


if __name__ == "__main__":
    print("hi")
