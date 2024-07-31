import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPT = """
You provide an answer to the user's question based on the provided context.
also specifically point to the relevant parts of the context.
"""
MODEL ="llama-3.1-70b-versatile"

def chat(messages: list[dict]):    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion


def run_query(query, context):

    if type(context) == str:

        context = f"Based on context: {context}\n"
        query = f"Answer the query: {query}\n"

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context + query}
        ]

        completion = chat(messages)

        answer = ""
        for chunk in completion:
            answer= answer + " " + chunk.choices[0].delta.content

        return answer

