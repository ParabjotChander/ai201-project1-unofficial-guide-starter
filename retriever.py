import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS
from ingest import chunked_documents

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(name=CHROMA_COLLECTION, 
                                               embedding_function=_ef, 
                                               metadata={"hnsw:space": "cosine"}
                                               )

def get_collection():
    return _collection

def embed_and_store(chunks):
    _collection.add(
        documents=[p['text'] for p in chunks],
        metadatas=[{"professor": p['professor'], "filename": p['filename']} for p in chunks],
        ids=[f"{p['filename']}-{p['chunk_index']}" for p in chunks]
    )
    print(f"Added {len(chunks)} chunks to ChromaDB collection '{CHROMA_COLLECTION}'.")

def retrieve(query, n_results=N_RESULTS):
    if _collection.count() == 0:
        #print(f"Collection '{CHROMA_COLLECTION}' is empty. No results to retrieve.")
        return []
    
    results = _collection.query(query_texts=[query], n_results=n_results, include=["documents", "metadatas", "distances"])
    
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []
    for doc, meta, dist in zip(docs, metadatas, distances):
        chunk = {
            "text": doc,
            "professor": meta["professor"] if isinstance(meta, dict) else None,
            "filename": meta["filename"] if isinstance(meta, dict) else None,
            "distance": dist
        }
        print(f"Retrieved chunk {chunk['text'][:50]}... from '{chunk['filename']}' with distance {chunk['distance']:.4f}")
        chunks.append(chunk)

    return chunks
""" 
get_collection()  # Ensure collection is initialized
embed_and_store(chunked_documents)  # Embed and store the chunked documents in Chroma
query1 = "How many questions are in Matthew Fried's test and how many minutes you have to complete them?"
retrieved_chunks = retrieve(query1)
print(f"retrieved_chunks: {retrieved_chunks} \n from query: {query1}")

query2 = "For Delaram Kahrobaei as a professor, you can understand the concepts through what?"
retrieved_chunks = retrieve(query2)
print(f"retrieved_chunks: {retrieved_chunks} \n from query: {query2}")

query3 = "What are the ways to pass Kent Boklan's class?"
retrieved_chunks = retrieve(query3)
print(f"retrieved_chunks: {retrieved_chunks} \n from query: {query3}")
"""