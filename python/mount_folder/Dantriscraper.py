import requests
from bs4 import BeautifulSoup
from Newscraper import Newscraper


class DantriScraper:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.base_url = "https://dantri.com.vn/tim-kiem/"
        self.urls = []

    def format_keyword(self):
        keys = self.keyword.split(" ")
        return "+".join(keys)


    def construct_url(self):
        formatted_keyword = self.format_keyword()
        return f"{self.base_url}{formatted_keyword}.htm?date=365&pi=1"


    def fetch_articles(self):
        url = self.construct_url()
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')


    def filter_by_keyword(self, limit=5):
        soup = self.fetch_articles()
        article_items = soup.find_all('article', class_='article-item', limit=limit)
        for article in article_items:
            a_tag = article.find('a')
            if a_tag and 'href' in a_tag.attrs:
                full_url = "https://dantri.com.vn" + a_tag['href']
                self.urls.append(full_url)


    def get_urls(self):
        return self.urls


    def print_url_content(self, url):
        response = requests.get(url)
        print(response.text)
    
    
    def export_mongodb(self, url):
        self.url = url
        self.init_new()
        self.store_in_mongodb()

def main():
    keyword = input("Please enter your keyword: ")
    scraper = DantriScraper(keyword)
    scraper.filter_by_keyword()
    urls: list = scraper.get_urls()
    for url in urls:
        newScraper: Newscraper = Newscraper(url)
        newScraper.init_new()
        newScraper.store_in_mongodb()
        
        
        
    

if __name__ == "__main__":
    main()
