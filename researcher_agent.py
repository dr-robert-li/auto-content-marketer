import asyncio
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
from webscout import AsyncWEBS

# Load environment variables from .env file
load_dotenv()

async def research_topic(topic_or_url):
    """
    Research a given topic or URL using webscout and Perplexity AI and provide relevant information.

    Args:
        topic_or_url (str): The topic or URL to research.

    Returns:
        dict: A dictionary containing the research results and references.
    """
    try:
        # Check if the input is a URL
        if topic_or_url.startswith("http://") or topic_or_url.startswith("https://"):
            # Extract the topic from the URL
            parsed_url = urlparse(topic_or_url)
            topic = parsed_url.path.strip("/").replace("-", " ")
        else:
            topic = topic_or_url

        # Create an AsyncWEBS instance
        async with AsyncWEBS() as webs:
            # Perform a news search using webscout
            news_results = await webs.news(
                topic,
                region="wt-wt",
                safesearch="off",
                timelimit="m",
                max_results=10
            )

            # Extract the summaries and references from the news search results
            news_summaries = []
            news_references = []
            for result in news_results:
                try:
                    news_summaries.append(result["summary"])
                    news_references.append(result["url"])
                except (KeyError, TypeError):
                    pass

            # Perform a text search using webscout
            text_results = await webs.text(
                topic,
                region="wt-wt",
                safesearch="off",
                timelimit="y",
                max_results=10
            )

            # Extract the summaries and references from the text search results
            text_summaries = []
            text_references = []
            for result in text_results:
                try:
                    text_summaries.append(result["summary"])
                    text_references.append(result["url"])
                except (KeyError, TypeError):
                    pass

        # Get the Perplexity AI API key from the environment variable
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

        # Search for the topic using Perplexity AI
        perplexity_api_url = "https://api.perplexity.ai/chat/completions"
        perplexity_payload = {
            "model": "sonar-medium-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise."
                },
                {
                    "role": "user",
                    "content": f"Provide a brief summary and relevant references for the topic: {topic}"
                }
            ]
        }
        perplexity_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {perplexity_api_key}"
        }
        perplexity_response = requests.post(perplexity_api_url, json=perplexity_payload, headers=perplexity_headers)
        perplexity_data = perplexity_response.json()

        # Extract the summary and references from the Perplexity AI response
        perplexity_summary = ""
        perplexity_references = []
        try:
            perplexity_summary = perplexity_data["choices"][0]["message"]["content"]
            # Extract references from the response if available
        except (KeyError, IndexError, TypeError):
            pass

        # Create a dictionary with the research results and references
        result = {
            "news_search": {
                "summaries": news_summaries,
                "references": news_references
            },
            "text_search": {
                "summaries": text_summaries,
                "references": text_references
            },
            "perplexity_ai": {
                "summary": perplexity_summary,
                "references": perplexity_references
            }
        }

        # Return the research results to app.py
        return result

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while researching the topic '{topic}': {e}")
        # Return an empty result dictionary to app.py
        return {
            "news_search": {
                "summaries": [],
                "references": []
            },
            "text_search": {
                "summaries": [],
                "references": []
            },
            "perplexity_ai": {
                "summary": "",
                "references": []
            }
        }

async def main(topic_or_url):
    result = await research_topic(topic_or_url)
    return result

def run_research(topic_or_url):
    return asyncio.run(main(topic_or_url))

