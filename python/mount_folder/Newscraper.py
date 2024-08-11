import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

class Newscraper:
    def __init__(self, url: str, db_name: str = "FPT-project", collection_name: str = "news"):
        self.url = url
        self.title: str = None
        self.author: str = None
        self.singular_sapo: str = None
        self.singular_content: list = []
        self.client = MongoClient("mongodb://docker.for.mac.host.internal:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_page(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, "html.parser")


    def parse_title(self, soup):
        title_tag = soup.find("h1", {"class": "title-page detail"})
        self.title = title_tag.string if title_tag else "No title found"


    def parse_author(self, soup):
        author_tag = soup.find("div", {"class": "author-name"})
        if author_tag:
            b_tag = author_tag.find("b")
            self.author = b_tag.string if b_tag else "No author found"
        else:
            self.author = "No author found"


    def parse_sapo(self, soup):
        sapo_tag = soup.find("h2", {"class": "singular-sapo"})
        self.singular_sapo = sapo_tag.string if sapo_tag else "No sapo found"


    def parse_content(self, soup):
        content_tag = soup.find("div", {"class": "singular-content"})
        if content_tag:
            self.singular_content = [p.string for p in content_tag.find_all("p") if p.string]
        else:
            self.singular_content = ["No content found"]


    def init_new(self):
        soup = self.fetch_page()
        self.parse_title(soup)
        self.parse_author(soup)
        self.parse_sapo(soup)
        self.parse_content(soup)


    def store_in_mongodb(self):
        document = {
            "title": self.title,
            "author": self.author,
            "sapo": self.singular_sapo,
            "content": self.singular_content,
            "url": self.url
        }
        self.collection.insert_one(document)
        print(f"Document inserted with title: {self.title}")

    def display(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Sapo: {self.singular_sapo}")
        print("Content:")
        for paragraph in self.singular_content:
            print(paragraph)
    
    
    

def main():
    url = input("Please enter the URL of the article: ")
    scraper = Newscraper(url)
    scraper.init_new()
    scraper.store_in_mongodb()
    scraper.display()

if __name__ == "__main__":
    main()

    