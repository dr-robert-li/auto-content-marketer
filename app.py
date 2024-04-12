import streamlit as st
import pyperclip
from scraper_agent import scrape_general_interests
from researcher_agent import run_research
from content_writer_agent import generate_content

# This needs a .env file with PERPLEXITY_API_KEY and OPENAI_API_KEY

def main():
    st.title("Auto Content Marketer")
    st.caption("This content generation app will scrape a social media profile (or any URL, really) to determine the general interests of the social media user, research a topic specified, then write content based on the general interests identified in the social media profile, the type of content you want to create, and the topic for the given channel.")
    social_media_url = st.text_input("Enter the social media profile URL (include HTTPS/HTTP prefix):")
    topic_or_url = st.text_input("Enter the topic:")
    channel = st.text_input("Enter the Channel (e.g. Facebook, LinkedIn, Instagram, Pinterest, Twitter, Blog, Email etc.):")
    content_type = st.text_input("Enter the Type of Content:", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="Advertisement, Sales Email, Thought Leadership, or Your Own")

    if 'content' not in st.session_state:
        st.session_state.content = ""

    if st.button("Generate Content"):
        if social_media_url and topic_or_url and channel:
            try:
                # Scrape general interests
                general_interests = scrape_general_interests(social_media_url)
                print(f"General Interests: {general_interests}")  # Debug print statement

                # Research the topic
                research_results = run_research(topic_or_url)
                print(f"Research Results: {research_results}")  # Debug print statement

                # Generate content
                st.session_state.content = generate_content(topic_or_url, channel, research_results, general_interests, content_type)
                print(f"Generated Content: {st.session_state.content}")  # Debug print statement

                # Display the generated content
                st.subheader("Generated Content")
                st.write(st.session_state.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please provide all the required inputs.")

    # Add a "Copy to Clipboard" button
    if st.session_state.content:
        if st.button("Copy to Clipboard"):
            pyperclip.copy(st.session_state.content)
            st.success("Content copied to clipboard!")

if __name__ == "__main__":
    main()
