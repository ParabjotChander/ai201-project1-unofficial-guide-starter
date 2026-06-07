from groq import Groq
from typer import prompt
from typer import prompt
from config import GROQ_API_KEY, LLM_MODEL
#from ingest import chunked_documents
#from retriever import retrieve, get_collection, embed_and_store

_client = Groq(api_key=GROQ_API_KEY)

format_chunks = lambda chunks: "\n\n".join(
    [f"{c['text']} (from {c['professor']})" for c in chunks]
)

def generate_response(query, retrieved_chunks):
    
    if not retrieved_chunks:
        return "I'm sorry, I couldn't find any relevant information to answer your question."
    
    prompt = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Use only the following retrieved rule chunks as context for your answer and cite the source. "
                    "If the answer isn't in the chunks, say you don't know instead of making something up."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{format_chunks(retrieved_chunks)}\n\n"
                    f"Question: {query}\n\n"
                    "Answer:"
                )
            }
        ]
    )
    
    return prompt.choices[0].message.content
"""
get_collection()  # Ensure collection is initialized
embed_and_store(chunked_documents)  # Embed and store the chunked documents in Chroma
query1 = "How many questions are in Matthew Fried's test and how many minutes you have to complete them?"
retrieved_chunks = retrieve(query1)
response = generate_response(query1, retrieved_chunks)
print(f"Response: {response} \n from query: {query1}")

query2 = "For Delaram Kahrobaei as a professor, you can understand the concepts through what?"
retrieved_chunks = retrieve(query2)
response = generate_response(query2, retrieved_chunks)
print(f"Response: {response} \n from query: {query2}")

query3 = "What are the ways to pass Kent Boklan's class?"
retrieved_chunks = retrieve(query3)
response = generate_response(query3, retrieved_chunks)
print(f"Response: {response} \n from query: {query3}")
"""