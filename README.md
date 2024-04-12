# Auto Content Marketer

Using the context of a given social media profile as well as a target use case, this tool will generate personalised content for content marketing purposes using OpenAI's GPT-4 and Perplexity's Sonnet Models for research.

It uses an agentic approach with content writer, researcher and scraper agents.

Install `requirements.txt`.
You will require your own OpenAI API Key and Perplexity API Key. Place these in a `.env` file e.g.

```
OPENAI_API_KEY="sk-********************************"
PERPLEXITY_API_KEY="pplx-********************************"
```

Run using `streamlit run app.py`