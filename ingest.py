import os
import random
from config import DOCS_PATH

def load_documents():
    documents = []
    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(".txt"):
            with open(os.path.join(DOCS_PATH, filename), "r") as file:
                text = file.read()
                professor_name = filename.replace(".txt", "").title()
                documents.append({
                    "professor": professor_name,
                    "filename": filename,
                    "text": text
                })
    print(f"Loaded {len(documents)} Professor Review documents. {[p['professor'] for p in documents]}")
    return documents

# Fixed Size Chunking: character-based chunking with a specified chunk size and overlap, 100 character per chunk and 20 character overlap
def chunk_text(text, chunk_size=250, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def chunk_documents():
    loaded_documents = load_documents()
    chunked_documents = []
    for doc in loaded_documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "professor": doc["professor"],
                "filename": doc["filename"],
                "chunk_index": i,
                "text": chunk
            })
    return chunked_documents

chunked_documents = chunk_documents()

print(f"Chunked documents into {len(chunked_documents)} chunks.")
'''
# 5 Random Chunks
print(f"Example chunk: {chunked_documents[random.randint(0, len(chunked_documents)-1)]['text']}\n")
print(f"Example chunk: {chunked_documents[random.randint(0, len(chunked_documents)-1)]['text']}\n")
print(f"Example chunk: {chunked_documents[random.randint(0, len(chunked_documents)-1)]['text']}\n")
print(f"Example chunk: {chunked_documents[random.randint(0, len(chunked_documents)-1)]['text']}\n")
'''