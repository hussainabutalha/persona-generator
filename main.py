import os
import praw
import google.generativeai as genai
import argparse
import json
from urllib.parse import urlparse
from dotenv import load_dotenv
from weasyprint import HTML

# Load environment variables from .env file
load_dotenv()

def setup_api_clients():
    """Initializes and returns authenticated clients for Reddit and Google AI."""
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    llm_client = genai.GenerativeModel('gemini-1.5-flash-latest')
    return reddit_client, llm_client

def scrape_reddit_data(reddit_client, username, limit=50):
    """Scrapes a user's recent posts and comments from Reddit."""
    print(f"🕵️ Scraping data for user: {username}...")
    try:
        redditor = reddit_client.redditor(username)
        activity_data = []
        for comment in redditor.comments.new(limit=limit // 2):
            activity_data.append(f"Comment: \"{comment.body}\"")
        for submission in redditor.submissions.new(limit=limit // 2):
            activity_data.append(f"Post: \"{submission.title} - {submission.selftext}\"")
        print(f"✅ Found {len(activity_data)} items.")
        return "\n---\n".join(activity_data)
    except Exception as e:
        print(f"❌ Error scraping user {username}: {e}")
        return None

def generate_persona_json(llm_client, user_data, username):
    """Generates a rich user persona as a JSON object using an LLM."""
    print("🧠 Generating rich user persona JSON with AI...")
    
    prompt = f"""
    Analyze the following Reddit data for the user '{username}' and generate a comprehensive user persona.
    Respond with ONLY a valid JSON object. Do not include markdown formatting or the word "json".
    The JSON object must have the following keys: "bio", "age", "occupation", "location", "personality", "behaviours", "goals", "motivations", "frustrations".

    - For "bio", write a short, 1-2 sentence summary of the user.
    - For "age", "occupation", and "location", use the string "Not mentioned" if no information is found.
    - For all other keys, the value must be an array of short, insightful strings (3-5 items per list).
    - Ensure every list is populated. If you have to make reasonable inferences, do so.

    Here is the data:
    ---
    {user_data}
    ---
    """
    try:
        response = llm_client.generate_content(prompt)
        # Clean up the response to ensure it's a valid JSON string
        cleaned_response = response.text.strip().replace("```json\n", "").replace("\n```", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"❌ Error generating or parsing persona JSON: {e}")
        return None
def create_pdf_persona(persona_data, username):
    """Creates a PDF persona from a data dictionary using an HTML template."""
    print("📄 Generating PDF from template...")
    try:
        with open('template.html', 'r') as f:
            template_str = f.read()

        # Format list items for HTML
        for key in ['personality', 'behaviours', 'goals', 'motivations', 'frustrations']:
            if key in persona_data and isinstance(persona_data[key], list):
                 persona_data[key] = "".join([f"<li>{item}</li>" for item in persona_data[key]])

        # Replace placeholders
        template_str = template_str.replace('{{USERNAME}}', username)
        for key, value in persona_data.items():
            template_str = template_str.replace(f"{{{{{key.upper()}}}}}", str(value))

        # Generate PDF
        if not os.path.exists('output'):
            os.makedirs('output')
        
        pdf_path = os.path.join('output', f'{username}_persona.pdf')
        HTML(string=template_str, base_url=os.path.dirname(os.path.abspath(__file__))).write_pdf(pdf_path)
        print(f"✅ PDF persona saved to: {pdf_path}")

    except Exception as e:
        print(f"❌ Error creating PDF: {e}")

def main():
    """Main function to orchestrate the script."""
    parser = argparse.ArgumentParser(description="Generate a Reddit user persona PDF from their profile URL.")
    parser.add_argument("url", type=str, help="The full URL of the Reddit user's profile.")
    args = parser.parse_args()

    try:
        path_parts = urlparse(args.url).path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'user':
            username = path_parts[1]
        else:
            raise ValueError
    except (ValueError, IndexError):
        print("❌ Invalid Reddit user URL format.")
        return

    reddit_client, llm_client = setup_api_clients()
    user_data = scrape_reddit_data(reddit_client, username)
    
    if user_data:
        persona_json = generate_persona_json(llm_client, user_data, username)
        if persona_json:
            create_pdf_persona(persona_json, username)

if __name__ == "__main__":
    main()