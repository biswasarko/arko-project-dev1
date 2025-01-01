import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="YOU ARE AN AGENT WHICH TRANSFORMS NATURAL LANGUAGE TO PANDAS QUERY."
                           "DDL OF TABLE:"
                           "DATE, gross_revenue, discount"
                           "THE TABLE CONTAINS DATE , gross revenue and discount OF A BUSINESS."
                           "THE OUTPUT SHOULD  only contain the pandas query",
)

chat_session = model.start_chat(
        history=[
                {
                        "role": "user",
                        "parts": [
                                "calculate year on year growth in net income\n",
                        ],
                },
                {
                        "role": "model",
                        "parts": [
                                "```json\n",
                                "{\n  \"query\": \"df['year'] = df['DATE'].dt.year;df['net_income_last_year'] = df.groupby('year')['NET_INCOME'].shift(1);df['YoY_growth'] = (df['NET_INCOME'] - df['net_income_last_year']) / df['net_income_last_year']\"\n}",
                                "\n```",
                        ],
                },
                {
                        "role": "user",
                        "parts": [
                                "calculate net revenue\n",
                        ],
                },
                {
                        "role": "model",
                        "parts": [
                                "The user wants to calculate the net revenue.\nNet revenue is calculated by subtracting the discount from the gross revenue.\nI need to create a new column 'net_revenue' by performing this subtraction.",
                                "```python\ndf['net_revenue'] = df['gross_revenue'] - df['discount']\n```",
                        ],
                },
        ]
)

# response = chat_session.send_message("INSERT_INPUT_HERE")

response = model.generate_content("Today we made 34000 in revenue and gave discount of 4000. insert this into the table")
print(response.text)

