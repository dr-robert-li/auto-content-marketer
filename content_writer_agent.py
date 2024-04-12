import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from the environment variable

def generate_content(topic, channel, research_results, general_interests, content_type):
    """
    Generate content based on the given topic, channel, research results, general interests, and content type.

    Args:
        topic (str): The topic to generate content for.
        channel (str): The channel or platform for which the content is being generated.
        research_results (dict): The research results and references related to the topic.
        general_interests (list): The list of general interests to consider while generating content.
        content_type (str): The type of content to generate (e.g., Advertisement, Sales, Thought Leadership, or Your Own).

    Returns:
        str: The generated content.
    """
    # Create the prompt for generating content
    prompt = f"""
    Generate content based on the following information:

    Topic: {topic}
    Channel: {channel}
    Research Results:
    {research_results}
    General Interests:
    {general_interests}
    Content Type: {content_type}

    Please provide content tailored to the given topic, channel, research results, and general interests. The content should achieve the content type. 

    If the channel is Facebook limit the content to 80 characters.
    If the channel is Twitter limit the content to 100 characters.
    If the channel is Instagram limit the content to 125 characters.
    If the channel is LinkedIn limit the content to 2000 words.
    If the channel is TikTok limit the content to 10 words.
    If the channel is Pinterest limit the content to 40 characters.
    If the channel is Youtube limit the content to 157 characters.
    If the channel is Blog limit the content to 2000 words.
    If the channel is Email limit the content to 150 words.

    If BOTH the Content Type is Sales AND the Channel is Email use the structure starting with a thanks for reading this email and then a sentence that starts with "I appreciate...", then a sentence starting with "Naturally...", then a sentence starting with "Obviously..." and then a sentence starting with "Typically..." that demonstrates an example of what other customers do, ending with a call to action to setup a meeting asking for suggested times and dates; within the body of the Email make sure to make specific reference to previous experience, or notable accomplishments from the General Interests; make the tone of the email fun; finally, in the Email Subject make specific reference to the person. AGAIN, make sure it is 150 WORDS OR LESS. Our lives depend on it.

    If the Content Type is Advertisement or Ad or Advert, include a call to action.

    DO NOT mention the content type in the content.
    DO NOT mention the general interests in the content.
    """

    # Generate the content using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are an expert content marketer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.7,
    )

    generated_content = response.choices[0].message['content'].strip()

    return generated_content
