from preprocessing import *
from sentiment_analysis import *
from crypto_data import *


if __name__ == "__main__":
    text_list = fetch_post()
    preprocessed_list = preprocess_text_list(
        text_list
    )  # format: (processed_text, [identifiers])
