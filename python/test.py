import google.generativeai as genai
from getpass import getpass
import json
import os
from dotenv import load_dotenv
import typing_extensions as typing
from tools import database_save, fetch_exchange_rate, search_openfoodfacts, search_web

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


# 1. Define the Schema ( Blueprint)
# We define exactly what a "BugReport" looks like.
class Bug(typing.TypedDict):
    description: str
    priority: str
    category: str  # e.g., UI, Backend, Content

class BugReport(typing.TypedDict):
    bugs: list[Bug]

# 2. Configure the Model
# We pass the 'response_schema' parameter. This forces the model to adhere to our class.
structured_model = genai.GenerativeModel(
    'gemini-2.5-flash',
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": BugReport
    }
)

# 3. Run the exact same input
user_email = """
Hi team, I found a couple of issues.
First, the login button is misaligned on mobile screens (High priority!).
Also, the 'about us' page has a typo in the header, but that's minor.
Lastly, the app crashes when I try to upload a PDF larger than 5MB.
"""

response = structured_model.generate_content(user_email)

# 4. Parse the Result
# Because we enforced JSON, we can safely load it without error handling.
data = json.loads(response.text)

print("---  DATA ---")
print(json.dumps(data, indent=4))

# DISCUSSION:
# Notice that for the 'PDF crash', the AI inferred the priority was likely 'High'
# or 'Medium' even though the user didn't explicitly say it.
# We now have a Python dictionary ready to be pushed to a database.

# To install: pip install tavily-python
from tavily import TavilyClient
client = TavilyClient("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")
response = client.search(
    query=""
)
print(response)

tool_model = genai.GenerativeModel(
    'gemini-2.5-flash',
    tools=[search_openfoodfacts, search_web]
)

# 2. Start a Chat Session (Automatic Mode)
# 'enable_automatic_function_calling=True' handles the loop for us:
# LLM wants tool -> Code runs tool -> Result sent back to LLM -> LLM answers user.

chat = tool_model.start_chat(enable_automatic_function_calling=True)