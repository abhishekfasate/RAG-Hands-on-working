from openai import OpenAI
from calculator import calculator
from file_reader import read_file
from memory import extract_memory, retrive_memory, memory
import json

def execute_tool_call(tool_call):
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print("TOOL:", tool_name)
    print("ARGUMENTS:", arguments)

    if tool_name=="calculator":
        return calculator(arguments["expression"])
    elif tool_name=="read_file":
        return read_file(arguments["file_path"])
    else:
        return f"Unknown tool: {tool_name}"
    
TOOLS = [
    {
        "type": "function",
        "function":{
            "name":"calculator",
            "description": """Perform arithmetic calculations.You MUST provide exactly one argument:'expression'.The expression must be a string containing the complete
                                arithmetic expression.
                Example:
                {"expression": "2 + 3"}

                Do NOT use arguments such as a, b, op.
            """,
            "parameters":{
                "type":"object",
                "properties":{
                    "expression":{
                        "type": "string",
                        "description": "The Arithmetic Expression To Calculate"
                    }
                },
                "required":["expression"]
            }
        }
    },
    {
            "type":"function",
            "function":{
                "name":"read_file",
                "description": "To Read Any File",
                "parameters":{
                    "type": "object",
                    "properties":{
                        "file_path":{
                            "type":"string",
                            "description":"Path of Text File to read"
                        }
                    },
                    "required":["file_path"]
                }
            }
    }
]

user_query = "What is my name"

extract_memory(user_message=user_query)

relevent_memeory = retrive_memory(user_query)

message = [
        {
            "role": "system",
            "content": """You are an assistant with access to tools.Use read_file when you need information from a file.Use calculator for arithmetic calculations.When a calculation is required, ALWAYS use the calculator tool.Do not perform arithmetic yourself.If the question is related to greet welcome or sentiment related to use casual reply."""
        },
        {
            "role": "system",
            "content": f"Relevant memory about the user: {relevent_memeory}"
        },
        {
             "role": "system",
            "content": """You are an assistant with access to memory.IMPORTANT MEMORY RULES:
                        - Use ONLY the provided relevant memory to answer questions about the user.
                        - Do NOT guess, infer, or assume information that is not explicitly present in memory.
                        - If the requested information is not present in the relevant memory, say:
                            "I don't know based on my memory."
                        - Never use unrelated memories to answer a question.
                    """
        },
        {  
            "role": "user",
            "content": user_query
        },
]

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Memory Update

while True:
    response = client.chat.completions.create(
        model= "llama3.1",
        tools=TOOLS,
        max_tokens=1024,
        stream= False,
        messages=message
    )

    answer = response.choices[0].message

    if not answer.tool_calls:
        print(answer.content)
        break

    if answer.tool_calls:
            tool_call = answer.tool_calls[0]

            result = execute_tool_call(tool_call)
        
            message.append(answer)

            message.append(
                {
                    "role": "tool",
                    "tool_call_id":answer.tool_calls[0].id,
                    "content": str(result)
                } 
            )