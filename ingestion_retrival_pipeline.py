import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

collection_name = "my_doc"
file_path = "tesla.txt"
model = SentenceTransformer("all-MiniLM-L6-v2") # Embeding Model
client = chromadb.PersistentClient("./chroma_db") # DB Connection or Creation
collection = client.get_or_create_collection(collection_name) # Table Creation

def load_text(file):
    with open(file=file,mode="r",encoding="utf-8") as f:
        print("File reading and returning")
        return f.read()

def chunking_file(content,chunk_size=500,overlap=50):
    step = chunk_size - overlap
    start = 0
    chunks = []

    while start < len(content):
        chunk = content[start:start+chunk_size]
        chunks.append(chunk)
        start = start+ step

    return chunks

def build_index(chunked_data):
    # Using Embedding model we are embedding the data into vector 
    embedding =model.encode(chunked_data).tolist()

    # Here we are adding that embeded data in to Our Vector DB which is croma DB under the so called table name my_doc
    collection.add(
        embeddings=embedding,
        documents=chunked_data,
        ids=[f"doc{i}" for i in range(len(chunked_data))],
        # This is require for Citation
        # metadatas=[
        #     {"source": file_path}
        #     for _ in chunked_data
        # ]
    )

def retrival_pipeline(query, top_k=2):
    query_embedding = model.encode([query]).tolist()
    result = collection.query(
        query_embeddings=query_embedding,
        n_results= top_k
    )
    
    return (result["documents"])

def llm_call(result_doc, query):
    client_llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    messages = []

    user_input = f"""
    Question: {query}

    Context:
        {result_doc}

    Answer the question directly and concisely using only the context.
    Do not say "according to the provided text" or similar phrases.
    """

    messages.append({"role": "user", "content": user_input})
    
    response = client_llm.chat.completions.create(
    model="llama3.1",
    messages=messages,
    stream=True,
    max_tokens=1024
)

    for chunk in response:
        delta = chunk.choices[0].delta.content

        if delta:
            print(delta, end="", flush=True)
    print()

if __name__== "__main__":
    # First Read The Files
    content = load_text(file=file_path)

    # Break the File in to chunks
    chunked_data = chunking_file(content)

    # Then Chunks Converted to vector
    build_index(chunked_data)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit","quit"):
            break
        
        result_doc = retrival_pipeline(user_input)
    
        llm_call(result_doc, user_input)

    
