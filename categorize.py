import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import numpy as np


def categorize_news():
    df = pd.read_csv('news_articles.csv') 

    categories = ['Politics', 'Sports', 'Technology', 'Health', 'Entertainment']
    np.random.seed(42)  
    df['Category'] = np.random.choice(categories, size=len(df)) 

    X = df['Summary'] 
    y = df['Category']  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = make_pipeline(CountVectorizer(), MultinomialNB())

    model.fit(X_train, y_train)

    predicted_categories = model.predict(X_test)

    df['Predicted Category'] = model.predict(df['Summary'])

    df.to_csv('categorized_news_articles.csv', index=False)

if __name__ == "__main__":
    categorize_news()