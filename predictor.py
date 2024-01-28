# This file generates a cryptocurrency investment recommendation and the confidence score for the prediction made.
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import precision_score
import ast
from TOP_CRYPTO import TOP_CRYPTO_TUPLES

df = pd.read_csv("./final.csv")


def predict():
    df["target"] = (df["percent_change"] > -0.2).astype(int)

    model = RandomForestClassifier(
        n_estimators=100, min_samples_split=50, random_state=1
    )

    train = df.iloc[:-20]
    test = df[:-20]

    predictors = ["compound"]

    model.fit(train[predictors], train["target"])

    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index)
    print("Confidence level: ", (precision_score(test["target"], preds)) * 100, "%")


def generate_recommendation(coin_recommendations):
    # TODO: generate recommendation
    for index, row in df.iterrows():
        if row["compound"] >= 0 and row["percent_change"] > -0.2:
            coin_recommendations.append(row)
    return coin_recommendations


def remove_duplicates(original_list):
    seen_elements = set()

    # Create an empty list to store the unique elements
    unique_list = []

    for item in original_list:
        equivalent_item = next(
            (e[0] for e in TOP_CRYPTO_TUPLES if item.lower() in [e.lower() for e in e]),
            item,
        )

        # Check if the equivalent item has been seen before
        if equivalent_item not in seen_elements:
            unique_list.append(equivalent_item)
            seen_elements.add(equivalent_item)
    return unique_list


if __name__ == "__main__":
    coin_recommendations = []

    rec = generate_recommendation(coin_recommendations)

    # rank them based on their percent change NOT compound score because that's just bias
    sorted_coin_recommendations = sorted(
        rec, key=lambda x: x["percent_change"], reverse=True
    )
    coin_names = []
    for i in range(len(sorted_coin_recommendations)):
        list_of_coins = ast.literal_eval(sorted_coin_recommendations[i]["coins"])
        for j in range(len(list_of_coins)):
            if list_of_coins[j] not in coin_names:
                coin_names.append(list_of_coins[j])

    final_recommendations = remove_duplicates(coin_names)
    print("Recommended crypto currencies to invest in:")
    for i in range(1, len(final_recommendations) + 1):
        print("{}. {}".format(i, final_recommendations[i - 1]))
    predict()
