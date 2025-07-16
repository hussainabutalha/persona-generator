import os
import praw
import google.generativeai as genai
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_api_clients():
    """
    Initializes and returns authenticated clients for Reddit and Google AI.
    """
    # Reddit PRAW client
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )

    # Google Generative AI client
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    llm_client = genai.GenerativeModel('gemini-1.5-flash-latest')

    return reddit_client, llm_client

def scrape_reddit_data(reddit_client, username, limit=50):
    """
    Scrapes a user's recent posts and comments from Reddit.
    
    Args:
        reddit_client: Authenticated PRAW client.
        username (str): The Reddit username to scrape.
        limit (int): The number of items to fetch.
        
    Returns:
        A formatted string containing the user's activity with citations.
    """
    print(f"🕵️ Scraping data for user: {username}...")
    try:
        redditor = reddit_client.redditor(username)
        activity_data = []

        # Scrape comments
        for comment in redditor.comments.new(limit=limit // 2):
            activity_data.append(
                f"Comment: \"{comment.body}\"\nSource: https://www.reddit.com{comment.permalink}\n"
            )

        # Scrape posts
        for submission in redditor.submissions.new(limit=limit // 2):
            activity_data.append(
                f"Post Title: \"{submission.title}\"\nPost Body: \"{submission.selftext}\"\nSource: {submission.url}\n"
            )
        
        print(f"✅ Found {len(activity_data)} items.")
        return "\n---\n".join(activity_data)
    except Exception as e:
        print(f"❌ Error scraping user {username}: {e}")
        return None

def generate_user_persona(llm_client, user_data, username):
    """
    Generates a user persona using an LLM based on scraped Reddit data.
    
    Args:
        llm_client: Authenticated Google AI client.
        user_data (str): Formatted string of user's posts and comments.
        username (str): The user's Reddit username.
        
    Returns:
        A string containing the generated user persona.
    """
    print("🧠 Generating user persona with AI...")
    
    prompt = f"""
    Based on the following Reddit posts and comments from the user '{username}', create a detailed user persona.
    For each characteristic you identify (e.g., interests, hobbies, occupation, personality traits, communication style), you MUST cite the specific source URL you used to make that inference.

    Follow this format strictly:
    **User Persona for /u/{username}**

    **1. Interest/Characteristic:** [Describe the interest or characteristic]
       - **Citation:** [Provide the full source URL]

    **2. Interest/Characteristic:** [Describe the next interest or characteristic]
       - **Citation:** [Provide the full source URL]

    Here is the data:
    ---
    {user_data}
    ---
    """
    
    try:
        response = llm_client.generate_content(prompt)
        print("✅ Persona generated successfully.")
        return response.text
    except Exception as e:
        print(f"❌ Error generating persona: {e}")
        return "Could not generate a persona for this user due to an API error."

def save_persona_to_file(username, persona_text):
    """Saves the generated persona to a text file."""
    if not os.path.exists('output'):
        os.makedirs('output')
    
    file_path = os.path.join('output', f'{username}_persona.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(persona_text)
    print(f"📄 Persona saved to: {file_path}")


def main():
    """Main function to orchestrate the script."""
    parser = argparse.ArgumentParser(description="Generate a Reddit user persona from their profile URL.")
    parser.add_argument("url", type=str, help="The full URL of the Reddit user's profile.")
    args = parser.parse_args()

    # Extract username from URL
    try:
        path_parts = urlparse(args.url).path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'user':
            username = path_parts[1]
        else:
            raise ValueError
    except (ValueError, IndexError):
        print("❌ Invalid Reddit user URL format. Please use a URL like: https://www.reddit.com/user/username/")
        return

    reddit_client, llm_client = setup_api_clients()
    
    user_data = scrape_reddit_data(reddit_client, username)
    
    if user_data:
        persona = generate_user_persona(llm_client, user_data, username)
        save_persona_to_file(username, persona)

if __name__ == "__main__":
    main()