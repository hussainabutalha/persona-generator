\# Reddit User Persona Generator



This script scrapes a Reddit user's recent posts and comments to generate a user persona using Google's Gemini Pro LLM. For each identified characteristic, it provides a citation to the specific post or comment it was derived from.



This project was created for the AI/LLM Engineer Intern assignment at BeyondChats.



\## Features



\- Scrapes user data via the official Reddit API (PRAW).

\- Generates a detailed user persona using a Large Language Model.

\- Cites the source for every piece of inferred information.

\- Saves the output to a clean `.txt` file.



\## Project Structure



```

.

├── .gitignore

├── main.py

├── requirements.txt

├── README.md

└── output/

&nbsp;   ├── kojied\_persona.txt

&nbsp;   └── Hungry-Move-6603\_persona.txt

```



\## Setup Instructions



\### 1. Clone the Repository



```bash

git clone <your-repo-url>

cd reddit-persona-generator

```



\### 2. Create a Virtual Environment



It is highly recommended to use a virtual environment.



```bash

\# Create the environment

python -m venv venv



\# Activate it

\# On Windows

.\\venv\\Scripts\\activate

\# On macOS/Linux

source venv/bin/activate

```



\### 3. Install Dependencies



```bash

pip install -r requirements.txt

```



\### 4. Set Up API Credentials



This script requires API access to both Reddit and Google AI.



1\.  \*\*Create a `.env` file\*\* in the root of the project directory.

2\.  \*\*Add your credentials\*\* to the file in the following format:



```env

REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=PersonaGenerator/0.1 by u/YourUsername
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
GOOGLE_API_KEY=your_google_api_key_here

\### Where to Find the Values
🤖 Reddit Credentials
You get these from the Reddit apps page.

Go to: https://www.reddit.com/prefs/apps

Scroll down and click "are you a developer? create an app..."

Fill out the form:

name: Give your app a name (e.g., AI Persona Tool).

type: Select script.

redirect uri: Type http://localhost:8080.

Click "create app".

Now you will see the values you need:

REDDIT_CLIENT_ID: This is the string of letters and numbers located directly under your app's name.

REDDIT_CLIENT_SECRET: This is the long string of characters next to the label secret.

REDDIT_USERNAME: This is simply your own Reddit username.

REDDIT_PASSWORD: Your own Reddit password.

REDDIT_USER_AGENT: This is a unique name you create for your script. It can be anything, but the format AppName/v1.0 by u/YourUsername is a good practice. Example: PersonaGenerator/0.1 by u/MyRedditAccount

> \*\*Note\*\*: The `.env` file is included in `.gitignore` and should not be committed to your public repository.



\## How to Execute the Code



Run the script from your terminal using the `main.py` file and provide the Reddit user's profile URL as a command-line argument.



\### Syntax

```bash

python main.py <URL\_of\_Reddit\_Profile>

```



\### Example

```bash

python main.py \[https://www.reddit.com/user/kojied/](https://www.reddit.com/user/kojied/)

```



The script will create a file named `<username>\_persona.txt` inside the `output/` directory.



\## Sample Outputs



Sample output files for the users `kojied` and `Hungry-Move-6603` are included in the `output/` directory as required by the assignment.

#   p e r s o n a - g e n e r a t o r 
 
 
