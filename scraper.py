import requests
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime 


def scrape_bbc():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    for item in soup.find_all("h2", class_ = 'sc-8ea7699c-3'): 
        title = item.get_text()
        anchor = item.find_parent('a')
        link = "https://www.bbc.com" + anchor.get('href')
        summary_text = item.find_parent('div', class_ = 'sc-8ea7699c-1').find_next_sibling('p')
        summary = summary_text.get_text() if summary_text else 'No summary available'
        pub_date = datetime.now().strftime("%Y-%m-%d")

        articles.append({
            "Title" : title,
            "Summary" : summary,
            "Publication Date" : pub_date,
            "Source" : "BBC",
            "URL" : link
        })
    
    return articles

def scrape_times_of_india():
    url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    for item in soup.find_all("div", class_="col_l_6"):
        title_element = item.find("figcaption")
        summary_element = item.find("p")
        link_element = item.find("a")

        if title_element and link_element:
            title = title_element.get_text(strip=True)
            link = link_element['href']
            summary = summary_element.get_text(strip=True) if summary_element else 'No summary available'
            pub_date = datetime.now().strftime("%Y-%m-%d")

            articles.append({
                "Title": title,
                "Summary": summary,
                "Publication Date": pub_date,
                "Source": "Times of India",
                "URL": link
            })

    return articles


if __name__ == "__main__":
    bbc_news = scrape_bbc()
    toi_news = scrape_times_of_india()
    new_articles_df = pd.DataFrame(bbc_news + toi_news)
    existing_articles_df = None
    try:
        existing_articles_df = pd.read_csv("news_articles.csv")
    except:
        pass
    combined_df = pd.concat([new_articles_df, existing_articles_df], ignore_index=True)
    combined_df.to_csv("news_articles.csv", index = False)