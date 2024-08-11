import requests
from bs4 import BeautifulSoup
import pandas as pd

def filter_by_keyword(key_word: str):
    # Format the keyword for the URL
    keys = key_word.split(" ")
    key_word = "+".join(keys)
    
    # Construct the URL
    url = f"https://dantri.com.vn/tim-kiem/{key_word}.htm?date=365&pi=1"
    
    # Make the HTTP request
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all article tags with the class 'article-item'
    article_items = soup.find_all('article', class_='article-item', limit=5)  # Only retrieve the first 5 items
    
    # Extract details from the articles
    article_data = []
    for article in article_items:
        title = article.find('h3', class_='article-item__title').get_text(strip=True)
        summary = article.find('div', class_='article-item__sapo').get_text(strip=True)
        a_tag = article.find('a')
        if a_tag and 'href' in a_tag.attrs:
            full_url = "https://dantri.com.vn" + a_tag['href']
            article_response = requests.get(full_url)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            article_content = article_soup.find('div', class_='dt-news__content').get_text(strip=True)
            article_data.append({
                'title': title,
                'summary': summary,
                'url': full_url,
                'content': article_content
            })
    return article_data


def main():
    key_word = input("Please enter your keyword: ")
    articles = filter_by_keyword(key_word)
    df = pd.DataFrame(articles)
    print(df)

if __name__ == "__main__":
    main()