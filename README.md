# Auto Content Marketer

Auto Content Marketer is a Python-based application that generates tailored content based on a given social media profile, topic, channel, and content type. It leverages web scraping, research, and AI-powered content generation to create engaging and relevant content for various platforms.

## Features
* Scrapes a social media profile (or any URL) to determine the general interests of the user
* Researches a specified topic using webscout and Perplexity AI
* Generates content based on the identified general interests, research results, channel, and content type
* Supports various channels, including Facebook, LinkedIn, Instagram, Pinterest, Twitter, Blog, and Email
* Provides specific content structures for sales emails
* Includes calls to action for advertisement content types

## Installation

* Clone the repository:

```
git clone https://github.com/your-username/auto-content-marketer.git
```

* Navigate to the project directory:

```
cd auto-content-marketer
```

* Install the required dependencies:

```
pip install -r requirements.txt
```

* Create a .env file in the project directory and add your API keys:

```
PERPLEXITY_API_KEY=your_perplexity_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage
* Run the Streamlit application:

```
streamlit run app.py
```

* Open the provided URL in your web browser.

Enter the required inputs:

1. Social media profile URL (including HTTPS/HTTP prefix)
2. Topic
3. Channel (e.g., Facebook, LinkedIn, Instagram, Pinterest, Twitter, Blog, Email)
4. Type of Content (e.g., Advertisement, Sales Email, Thought Leadership, or Your Own)

* Click the "Generate Content" button to generate the content based on the provided inputs.

* The generated content will be displayed on the screen. You can copy the content to the clipboard by clicking the "Copy to Clipboard" button.

## File Structure

* `app.py`: The main Streamlit application file that handles user input and orchestrates the content generation process.
* `scraper_agent.py`: Contains the ScraperAgent class responsible for scraping general interests from a given URL.
* `researcher_agent.py`: Provides functions to research a topic using webscout and Perplexity AI.
* `content_writer_agent.py`: Generates content based on the topic, channel, research results, general interests, and content type using the OpenAI API.
* `requirements.txt`: Lists the required Python dependencies for the project.

## Dependencies
The project relies on the following key dependencies:

* Streamlit: A framework for building interactive web applications in Python.
* BeautifulSoup: A library for parsing HTML and XML documents.
* Selenium: A tool for automating web browsers.
* OpenAI: An API for accessing powerful language models for content generation.
* webscout: A library for performing web searches and retrieving results.
* Perplexity AI: An API for generating summaries and retrieving relevant information.

For a complete list of dependencies, please refer to the requirements.txt file.