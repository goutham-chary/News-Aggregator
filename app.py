from flask import Flask, render_template, request
from categorize import categorize_news
from scraper import main
import pandas as pd
import os
import threading

app = Flask(__name__)


if not os.path.exists("news_articles.csv"):
    df = pd.DataFrame(columns=["Title", "Summary", "Publication Date", "Source", "URL"])
    df.to_csv("news_articles.csv", index=False)

if not os.path.exists("categorized_news_articles.csv"):
    main()  
    categorize_news()

def load_news_data():
    try:
        return pd.read_csv('categorized_news_articles.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Title', 'Summary', 'Publication Date', 'Source', 'URL', 'Predicted Category'])

df = load_news_data()

@app.route('/')
def index():
    selected_category = request.args.get('category', default='All')

    if selected_category != 'All':
        filtered_news = df[df['Predicted Category'] == selected_category]
    else:
        filtered_news = df

    categories = df['Predicted Category'].unique()

    return render_template('index.html', news=filtered_news.to_dict(orient='records'), categories=categories, selected_category=selected_category)

def update_news():
    main() 
    categorize_news()  
    global df
    df = load_news_data()  

if __name__ == '__main__':
    threading.Thread(target=update_news, daemon=True).start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
