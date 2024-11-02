from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the categorized news articles
df = pd.read_csv('categorized_news_articles.csv')  # Ensure this CSV file exists

@app.route('/')
def index():
    # Get the selected category from the request
    selected_category = request.args.get('category', default='All')

    # Filter the DataFrame based on the selected category
    if selected_category != 'All':
        filtered_news = df[df['Predicted Category'] == selected_category]
    else:
        filtered_news = df

    # Get unique categories for the filter
    categories = df['Predicted Category'].unique()

    return render_template('index.html', news=filtered_news.to_dict(orient='records'), categories=categories, selected_category=selected_category)

if __name__ == '__main__':
    app.run(debug=True)