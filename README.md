# 🪙 r/CryptoCurrency Investment Recommender 🚀

### How to run my project:
1. Run ```preprocessing.py```
2. Run ```sentiment_analysis.py```
3. Run ```crypto_data.py```
4. Run ```predictor.py```

You must have your own API keys and secret keys from the Reddit API, Coinbase Pro API, and a password for your Reddit account in a .env file.

---
# Abstract
I've always been interested in investing in crypto, but I never knew which one to invest in. As a CS student, I knew I had to leverage my knowledge to easily gain insights into the best crypto currencies to invest in. This project collects data from the subreddit r/CryptoCurrency and checks what people are saying about certain cryptocurrencies, compares it to the actual crypto market, and generates a list of recommended cryptocurrencies to invest in.

You might wonder, why Reddit? My answer is, Reddit has unfiltered information from people with actual experience in investing. I could get data from well-known organizations and the news, but as you already know, the government is evil and is trying to brainwash you through mass media. Just kidding, but I think it's more insightful to hear what people are directly saying about certain crytpocurrencies than just to follow the mass media. The following are the details of each step of my project.

---

# I. Data Collection
I was planning on using Pushshift API to fetch data from Reddit because it allows you to fetch a large amount of data, but as of April 2023, Reddit decided turn off Pushshift API's access to Reddit's data API as written [here](https://www.reddit.com/r/modnews/comments/134tjpe/reddit_data_api_update_changes_to_pushshift_access/) due to the violation of their Data API terms.

So I decided to directly use the Reddit API, which unfortunately has data fetching limitations. I can fetch the data within a loop, but that locks my account for exceeding the rate limit.

After fetching the posts, a CSV file is created with all of the posts. The file contains the following information:
* Subreddit name
* Title
* Body
* Upvote ratio
* Upvote count
* Downvote count
* Score
* Date/Time created

---

# II. Data Preprocessing 
I preprocessed the data fetched by removing non-alphabet character, removing links, tags, and [stop words](https://en.wikipedia.org/wiki/Stop_word#:~:text=Stop%20words%20are%20the%20words,text%29%20because%20they%20are%20insignificant.), and [stemming](https://en.wikipedia.org/wiki/Stemming#:~:text=In%20linguistic%20morphology%20and%20information,generally%20a%20written%20word%20form.) them. The stop words are from the NLTK corpus package, and the Porter Stemming algorithm is used for stemming the words. These operations are performed on the text AND the title of the post because both could provide insight into the sentiment of the post.

Additionally, another column is appended to the CSV file called 'coins' which contains a list of all the cryptocurrencies mentioned in each post. I did this by getting a JSON file of the top 50 cryptocurrencies and stored them in a global variable to be reused anywhere else in the project. This will be later used to associate a cryptocurrency to each post.
<p align='center'>
<img width="800" alt="Screenshot 2024-01-28 at 16 28 38" src="https://github.com/samuelhan713/r-CryptoCurrency_Data_Analysis/assets/60247381/f87b4faa-feea-41ee-9499-b96b60c0ce10">
</p>

---

# III. Sentiment Analysis
This step is an essential step because it determines whether a post is talking positively or negative about a cryptocurrency. I used the NLTK sentiment analyzer library to analyze the post, which is known to use a [Naive Bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier).

I also tried using Valence Aware Dictionary for Sentiment Reasoning also known as the VADER model, but I encountered several errors since VADER is made more for specific types of textual data while the basic NLTK sentiment analyzer is more for general data. 

The NLTK sentiment analyzer assigns 4 values to a piece of text: pos (positive), neu (neutral), neg (negative), and compound. Pos, neu, and neg values range from 0 to 1, and compound ranges from -1 to 1, inclusive. The higher the number, the more the text is of that value. In other words, a positive statement will be assigned a high pos value like 0.9 and a low neg value. If a statement isn't positive nor negative, it is assigned a high neu value. The positive text will be assigned a positive compound value, while a negative text will be assigned a negative compound value.

Finally, the original CSV is merged with the sentiment intensity data and exported again.
<p align='center'>
<img width="800" alt="Screenshot 2024-01-28 at 16 31 56" src="https://github.com/samuelhan713/r-CryptoCurrency_Data_Analysis/assets/60247381/3e11af9c-2b6f-46ac-9575-8057aa8a513f">
</p>

Here's a graph that I made with matplotlib, comparing the compound score for each post:
<p align='center'>
<img width="800" alt="Screenshot 2024-01-26 at 19 30 41" src="https://github.com/samuelhan713/r-CryptoCurrency_Data_Analysis/assets/60247381/406cd4ad-be04-4606-b77f-10730850783d">
</p>

---

# IV. Crypto Market Analysis
I used the Coinbasepro API to fetch live and historical data of the trends of any type of cryptocurrency available on Coinbase. I calculated the percent change in the price of a cryptocurrency from a specific date to now in order to determine whether it increased or decreased in price. If the percent change is positive, we’ll want to recommend that currency more than one that has a negative percent change. If you like formulas, this is what it looks like:

```
Percent change = ((price of specified date - current price) / price of specificed data) * 100
```

I appended a new column to the CSV file called 'percent_change' that carries the percent change of each currency a post mentions. Since there could be more than 1 currency mentioned in a post, it calculates the average of all the percent changes and uses that value.

Problem faced: for some reason, there were some currencies mentioned in a post that were non-existent in the Coinbase API, causing a fetching error. As a temporary solution, I just exlcuded that currency from the TOP_CRYPTO.py file so that it won't be identified as a valid currency.

# V. Training / Testing and Generating Recommendations
Now for the fun part.
I used a [random forest classifier](https://en.wikipedia.org/wiki/Random_forest) model to train and test my data because my data is not very good and random forest is good for handling noisy data and is robust to overfitting. For the last time, I added another column to the current data called "target" which is assigned a value of 1 if the percent change is > 0 and 0 if the percent change is < 0. 

**How I generated recommendations: if a currency is talked positively about (high compound score) and the price of that currency is increased from the date that post about that currency was made to now, then it should be recommended.**

I didn’t include the sentiment score when determining whether to recommend a currency because two posts could be talking positively about a post, but one of the posts could also include something negative about another coin, affecting the sentiment score. Also, the intensity of the sentiment could be subjective and unreliable. Therefore, the model becomes inaccurate with more currency mentioned in a post.

With the data I have now, I was able to achieve a confidence level of up to **85.7%**.
Here's an example:
<p align="center">
<img width="500" alt="Screenshot 2024-01-28 at 18 10 56" src="https://github.com/samuelhan713/r-CryptoCurrency_Data_Analysis/assets/60247381/a80e4787-f244-4070-9093-39ac5b196125">
</p>


---

# Closing Thoughts
I don't have much data as mentioned earlier because there are rate limits to the Reddit API. If I get access to more data, the reliability of my model will increase. Once I'm able to gain access to a large dataset, I will be able to use this project to actually invest in cryptocurrencies to buy.
I am planning to create a UI for this project so that anyone will be able to access it and gain useful insights to currencies to invest in with a few clicks.
