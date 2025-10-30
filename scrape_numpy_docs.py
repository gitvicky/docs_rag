"""
NumPy Documentation Scraper and Indexer
Downloads NumPy documentation and creates a vector database for RAG
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path
import json

class NumpyDocScraper:
    def __init__(self, base_url="https://numpy.org/doc/stable/"):
        self.base_url = base_url
        self.visited_urls = set()
        self.docs = []
        
    def is_valid_url(self, url):
        """Check if URL is valid numpy doc URL"""
        parsed = urlparse(url)
        return (
            parsed.netloc in ["numpy.org", ""] and
            "/doc/stable/" in url and
            not url.endswith(('.pdf', '.zip', '.tar.gz')) and
            '#' not in url  # Skip anchor links
        )
    
    def clean_text(self, soup):
        """Extract and clean text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def scrape_page(self, url):
        """Scrape a single page"""
        if url in self.visited_urls:
            return []
        
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            self.visited_urls.add(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title = title.get_text() if title else url
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='body')
            if main_content:
                content = self.clean_text(main_content)
            else:
                content = self.clean_text(soup)
            
            # Only add if there's substantial content
            if len(content) > 200:
                self.docs.append({
                    'url': url,
                    'title': title,
                    'content': content
                })
            
            # Find all links to other docs
            links = []
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                    links.append(full_url)
            
            return links
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def scrape_docs(self, max_pages=50, delay=0.5):
        """Scrape NumPy documentation"""
        to_visit = [self.base_url]
        pages_scraped = 0
        
        # Key pages to prioritize
        priority_pages = [
            "reference/routines.html",
            "reference/arrays.html",
            "user/basics.html",
            "user/absolute_beginners.html",
        ]
        
        # Add priority pages to front of queue
        for page in priority_pages:
            to_visit.insert(0, urljoin(self.base_url, page))
        
        while to_visit and pages_scraped < max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            new_links = self.scrape_page(url)
            to_visit.extend(new_links)
            
            pages_scraped += 1
            time.sleep(delay)  # Be nice to the server
            
            if pages_scraped % 10 == 0:
                print(f"Progress: {pages_scraped}/{max_pages} pages scraped")
        
        print(f"\nTotal pages scraped: {len(self.docs)}")
        return self.docs
    
    def save_docs(self, filepath="numpy_docs.json"):
        """Save scraped docs to JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.docs)} documents to {filepath}")


if __name__ == "__main__":
    print("NumPy Documentation Scraper")
    print("=" * 60)
    
    scraper = NumpyDocScraper()
    docs = scraper.scrape_docs(max_pages=100, delay=0.5)
    scraper.save_docs("numpy_docs.json")
    
    print("\nDone! Now run build_vector_db.py to create the vector database.")
