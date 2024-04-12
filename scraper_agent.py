import requests
from bs4 import BeautifulSoup
import re
from researcher_agent import research_topic
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ScraperAgent:
    def __init__(self):
        self.scraped_data = []
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.1"
        self.driver = self.setup_driver()

    def setup_driver(self):
        """
        Set up the Selenium web driver with Chrome options.
        """
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode

        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def scrape_website(self, url):
        """
        Scrape the website at the given URL.
        """
        print(f"Scraping: {url}")

        try:
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Extract relevant data from the page
            title = self.extract_title(soup)
            description = self.extract_description(soup)
            date = self.extract_date(soup)
            content = self.extract_content(soup)

            # Store the scraped data
            self.scraped_data.append({
                'url': url,
                'title': title,
                'description': description,
                'date': date,
                'content': content
            })

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    def extract_title(self, soup):
        """
        Extract the title from the HTML soup.
        """
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        return ''

    def extract_description(self, soup):
        """
        Extract the description from the HTML soup.
        """
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            return meta_description.get('content', '').strip()
        return ''

    def extract_date(self, soup):
        """
        Extract the date from the HTML soup.
        """
        date_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
        date_match = date_pattern.search(soup.get_text())
        if date_match:
            return date_match.group()
        return ''

    def extract_content(self, soup):
        """
        Extract the main content from the HTML soup.
        """
        content_tag = soup.find('body')
        if content_tag:
            return content_tag.get_text().strip()
        return ''

    def close_driver(self):
        """
        Close the Selenium web driver.
        """
        self.driver.quit()

def scrape_general_interests(url):
    """
    Scrape general interests from the given URL and summarize the scraped data using GPT-4.
    """
    scraper = ScraperAgent()
    try:
        scraper.scrape_website(url)
        scraper.close_driver()

        # Summarize the scraped data using GPT-4
        scraped_data_summary = summarize_with_gpt4(scraper.scraped_data)
        return scraped_data_summary

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        print("Passing the URL to researcher_agent.py")
        research_result = research_topic(url)
        return research_result

def summarize_with_gpt4(scraped_data):
    """
    Summarize the scraped data using GPT-4.
    """
    # Combine the scraped data into a single string
    scraped_data_text = "\n".join([
        f"URL: {data['url']}\nTitle: {data['title']}\nDescription: {data['description']}\nDate: {data['date']}\nContent: {data['content']}"
        for data in scraped_data
    ])

    # Get the OpenAI API key from the environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Call the GPT-4 API to summarize the scraped data
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes scraped website data."},
            {"role": "user", "content": f"Please summarize the following scraped data making particular note of the most recent posts and job or work experience:\n{scraped_data_text}"}
        ]
    )

    # Extract the summary from the API response
    summary = response.choices[0].message['content'].strip()

    return summary
