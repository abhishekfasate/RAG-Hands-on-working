from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

memory = ["My Name Abhishek"]

def retrive_memory(user_query):
    relevant_memory = []

    for item in memory:
        if any (word.lower() in item for word in user_query.split(" ")):
            relevant_memory.append(item)

    return relevant_memory

def extract_memory(user_message):
    prompt = f"""
        You are NOT a chatbot.
        You are a memory extraction function.

        Your ONLY job is to extract explicit facts from the user's message.

        IMPORTANT:
        - Never talk to the user.
        - Never ask questions.
        - Never explain anything.
        - Never say "I'll follow the rules".
        - Never invent or infer facts.
        - A question is NOT a fact.
        - If there is no explicit fact, output exactly: NONE
        - Otherwise output ONLY the fact.

        Examples:

        User: My name is Abhishek
        Output: User's name is Abhishek

        User: My girlfriend's name is Shivani
        Output: User's girlfriend's name is Shivani

        User: What is my name?
        Output: NONE

        User: How are you?
        Output: NONE

        User message:
        {user_message}

        Output:
    """

    response = client.chat.completions.create(
        model="llama3.1",
        stream=False,
        max_tokens=1024,
        messages=[{
            "role":"user",
            "content": prompt
        }]
    )

    result = response.choices[0].message.content

    if result!=None:
        memory.append(result)

    print("The Original Memory is:\n",memory)