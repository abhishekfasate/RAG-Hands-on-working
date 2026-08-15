# Custom RAG & Agentic Tooling Sandbox

A lightweight, hands-on implementation of **RAG and AI Agent concepts built completely from scratch in Python**. The purpose of this repository is to understand what happens behind frameworks such as **LangChain and LangGraph**, rather than hiding the core workflow behind abstractions.

The repository currently covers:

* End-to-end RAG pipeline
* Document ingestion and chunking
* Text embeddings
* ChromaDB vector storage
* Semantic retrieval
* LLM-based question answering using retrieved context
* Function calling
* Tool calling
* Multi-step agentic tool execution
* Agent memory for user-specific information

> **Important:** The implementations are intentionally built without LangChain or LangGraph to understand the underlying concepts and workflows first.

---

## 1. RAG — Retrieval-Augmented Generation

The RAG pipeline in this repository demonstrates how an LLM can answer questions using information stored in predefined documents such as `.txt` and `.pdf` files.

### Overall RAG Flow

```text
Documents
   ↓
File Reading
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Vector Database (ChromaDB)
```

Then, when the user asks a question:

```text
User Query
   ↓
Query Embedding
   ↓
Similarity Search
   ↓
Top-K Relevant Chunks
   ↓
Original Text / Context
   ↓
LLM
   ↓
Answer
```

---

## 2. Document Ingestion Pipeline

The ingestion pipeline is responsible for converting raw documents into searchable vector data.

### Step 1 — Read Documents

The repository contains a file-reading component:

```text
file_reader.py
```

It is responsible for reading the source documents and extracting their text.

The pipeline can work with document data such as:

```text
.txt
.pdf
```

---

### Step 2 — Chunking

Large documents cannot simply be treated as one large piece of text.

The extracted document text is therefore divided into smaller chunks.

```text
Original Document
        ↓
   Text Extraction
        ↓
      Chunking
        ↓
 ┌───────────────┐
 │ Chunk 1       │
 │ Chunk 2       │
 │ Chunk 3       │
 │ ...           │
 └───────────────┘
```

Chunking makes it possible to retrieve only the relevant portions of a document instead of passing the entire document to the LLM.

The repository initially implements the chunking logic manually to understand how chunking works before relying on framework abstractions.

---

### Step 3 — Generate Embeddings

Each chunk is converted into a numerical vector representation called an **embedding**.

Conceptually:

```text
"Tesla was founded in..."
            ↓
      Embedding Model
            ↓
[0.12, -0.43, 0.78, ...]
```

The embedding represents the semantic meaning of the text.

This allows semantically similar pieces of text to be compared mathematically.

---

### Step 4 — Store Embeddings in ChromaDB

The generated embeddings are stored in **ChromaDB**, along with the corresponding document/chunk information and metadata.

```text
Chunk
  ↓
Embedding
  ↓
ChromaDB
```

The vector database allows the system to efficiently search for chunks that are semantically similar to a user's query.

---

## 3. RAG Retrieval Pipeline

The retrieval pipeline is the second major part of the RAG implementation.

When the user asks a question, the system does not directly send the question to the LLM.

Instead, it first searches the vector database for relevant information.

### Retrieval Flow

```text
User Question
      ↓
Generate Query Embedding
      ↓
Search ChromaDB
      ↓
Similarity Matching
      ↓
Retrieve Top-K Chunks
      ↓
Extract Original Text
      ↓
Build Context
      ↓
Send Context + Question to LLM
      ↓
Generate Answer
```

### Example

Suppose the knowledge base contains information about Tesla.

The user asks:

```text
"When was Tesla founded?"
```

The system first converts the question into an embedding:

```text
User Query
    ↓
Embedding Model
    ↓
Query Vector
```

That vector is then compared against the vectors stored in ChromaDB.

The most relevant chunks are retrieved:

```text
Top-K Results

Chunk 1 → Highly relevant
Chunk 2 → Relevant
Chunk 3 → Somewhat relevant
```

The original text from these chunks is then provided to the LLM as context.

```text
System Prompt
+
Retrieved Context
+
User Question
        ↓
       LLM
        ↓
     Answer
```

This allows the LLM to answer using the information contained in the provided knowledge base rather than relying only on its pretrained knowledge.

---

## 4. Complete RAG Architecture

The complete implementation can be represented as:

```text
                    OFFLINE / INGESTION
                    -------------------

          TXT / PDF Documents
                  ↓
             File Reader
                  ↓
               Chunking
                  ↓
            Embedding Model
                  ↓
              Embeddings
                  ↓
              ChromaDB
                  │
                  │
                  ▼
                    ONLINE / RETRIEVAL
                    -------------------

             User Question
                  ↓
            Query Embedding
                  ↓
          Similarity Search
                  ↓
          Top-K Relevant Chunks
                  ↓
          Original Chunk Text
                  ↓
             Context Builder
                  ↓
           Context + Question
                  ↓
                  LLM
                  ↓
               Answer
```

---

# 5. AI Agent Implementation

The second major part of this repository focuses on **AI Agents**.

The goal was to understand how an agent can decide when to use external tools and how the result of one tool can become the input for another step.

The agent implementation covers:

* Function calling
* Tool calling
* Tool execution
* Multi-step tool loops
* Agent memory

---

## 6. Function / Tool Calling

The repository implements function/tool calling so that the LLM can request execution of deterministic operations instead of trying to perform everything itself.

For example, mathematical calculations should be handled by a calculator rather than relying on the LLM to estimate or reason through arithmetic.

The calculator is implemented in:

```text
calculator.py
```

Conceptually:

```text
User
 ↓
LLM
 ↓
"Use calculator"
 ↓
Tool Selection
 ↓
calculator.py
 ↓
Calculation Result
 ↓
LLM
 ↓
Final Answer
```

This demonstrates the basic idea behind modern LLM tool calling.

---

# 7. Multi-Step Agentic Tool Loop

The repository also implements a **multi-step reasoning/tool execution loop**.

The important concept is that an agent does not necessarily need to finish its task with one tool call.

The output of one tool can become the input/context for the next tool.

For example:

```text
User Request
     ↓
     LLM
     ↓
   Tool A
     ↓
 Tool A Result
     ↓
     LLM
     ↓
   Tool B
     ↓
 Tool B Result
     ↓
     LLM
     ↓
 Final Answer
```

This creates an iterative agent loop:

```text
Think / Decide
      ↓
Select Tool
      ↓
Execute Tool
      ↓
Receive Result
      ↓
Decide Next Action
      ↓
Select Another Tool
      ↓
Execute
      ↓
...
      ↓
Final Response
```

This is an important foundation for understanding how agent frameworks implement tool execution internally.

---

# 8. Agent Memory

The repository also contains an implementation of **memory for agents**.

The purpose is to allow the agent to retain user-specific information across interactions.

Conceptually:

```text
User
 ↓
Conversation
 ↓
Extract / Store Relevant Information
 ↓
Memory
 ↓
Future Conversation
 ↓
Retrieve Relevant Memory
 ↓
Use Memory in Response
```

For example, if the user provides a personal fact, that information can be stored and later retrieved when required.

This demonstrates the difference between:

```text
LLM Context
```

and

```text
Persistent / External Memory
```

The memory is managed outside the model itself and supplied to the agent when relevant.

---

# 9. RAG vs Agent

The repository intentionally demonstrates both concepts separately.

### RAG

RAG focuses on:

```text
Retrieve Information
        ↓
Give Information to LLM
        ↓
Generate Answer
```

Its primary purpose is to provide the LLM with relevant external knowledge.

### Agent

An agent focuses on:

```text
Understand Task
      ↓
Decide Action
      ↓
Use Tool
      ↓
Observe Result
      ↓
Decide Next Action
      ↓
Repeat
      ↓
Final Answer
```

Its primary purpose is to allow the LLM to interact with tools and perform multi-step tasks.

---

# 10. Why Everything Was Built From Scratch

This repository intentionally avoids using:

```text
LangChain
LangGraph
```

for the core implementations.

The goal was to understand the underlying mechanisms before learning framework abstractions.

Instead of directly using:

```text
LangChain Retriever
LangChain Agent
LangChain Memory
LangGraph Workflow
```

the core workflows were implemented manually using Python.

This provides a better understanding of:

* What actually happens during ingestion
* How chunking works
* How embeddings are generated
* How vectors are stored
* How similarity search works
* How retrieved context reaches the LLM
* How function calling works
* How tools are selected and executed
* How tool results are fed back into the agent
* How multi-step agent loops work
* How external memory can be maintained

---

# 11. Technical Stack

| Layer                | Technology       | Purpose                                |
| -------------------- | ---------------- | -------------------------------------- |
| Programming Language | Python           | Core implementation                    |
| Document Processing  | Custom Python    | File reading and text processing       |
| Ingestion            | Custom Python    | Chunking and preprocessing             |
| Embeddings           | Embedding Model  | Convert text into vectors              |
| Vector Database      | ChromaDB         | Store and search embeddings            |
| LLM                  | OpenAI API       | Generation and function/tool calling   |
| Agent Tools          | Python Functions | External deterministic operations      |
| Calculator           | `calculator.py`  | Deterministic arithmetic               |
| File Reader          | `file_reader.py` | Document ingestion                     |
| Environment          | `python-dotenv`  | Environment variable management        |
| Framework            | None             | Core concepts implemented from scratch |

---

# 12. Repository Learning Progress

### RAG

* [x] Document ingestion
* [x] File reading
* [x] Text extraction
* [x] Text chunking
* [x] Embedding generation
* [x] Vector database setup
* [x] Store embeddings in ChromaDB
* [x] Query embedding
* [x] Similarity search
* [x] Top-K retrieval
* [x] Retrieve original chunk text
* [x] Pass retrieved context to LLM
* [x] Generate answers using retrieved context
* [x] End-to-end RAG pipeline

### AI Agents

* [x] Function calling
* [x] Tool calling
* [x] Tool execution
* [x] Calculator tool
* [x] Multi-step tool execution loop
* [x] Passing output from one tool to the next step
* [x] Agent memory
* [x] User-specific memory retrieval

### Frameworks

* [x] Core concepts implemented without frameworks
* [ ] LangChain
* [ ] LangGraph

The framework implementations are intentionally kept for the next stage, after understanding the underlying concepts from scratch.

---

# 13. Main Learning Objective

The main objective of this repository is **not just to build an application**, but to understand the architecture behind modern LLM applications.

The progression is:

```text
Python
  ↓
LLM APIs
  ↓
Embeddings
  ↓
Vector Databases
  ↓
RAG
  ↓
Function Calling
  ↓
Tool Calling
  ↓
Multi-Step Agents
  ↓
Agent Memory
  ↓
LangChain / LangGraph
```

By implementing the lower-level workflow first, the abstractions provided by frameworks such as LangChain and LangGraph can be understood as tools that simplify already-understood concepts rather than as black boxes.

---

## 14. Repository Summary

This repository is a **from-scratch Python implementation of RAG and AI Agent fundamentals**.

It contains two major areas:

### RAG

```text
Documents
→ Chunking
→ Embeddings
→ ChromaDB
→ Query Embedding
→ Similarity Search
→ Top-K Context
→ LLM
→ Answer
```

### AI Agents

```text
User Request
→ LLM
→ Tool Selection
→ Tool Execution
→ Tool Result
→ Next Decision
→ Additional Tool
→ Final Answer
```

Along with:

```text
Agent
+
Memory
→
User-Specific Context
```

The repository therefore provides the foundation required to move from **building LLM applications from scratch** to understanding and using higher-level frameworks such as **LangChain and LangGraph**.
