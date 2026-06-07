import gradio as gr
from ingest import chunk_documents
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response

def run_ingestion():
    chunked_documents = chunk_documents()
    collection = get_collection()  # Ensure collection is initialized
    embed_and_store(chunked_documents)  # Embed and store the chunked documents in Chroma
    return f"Ingested {len(chunked_documents)} chunks into the vector database."

# Handle user query and generate response, the source is in the reponse as well, grounding instructions are in the generator.py file
def handle_query(message):
    if not message.strip():
        return "Ask a question to get started!", ""
    retrieved_chunks = retrieve(message)
    return generate_response(message, retrieved_chunks)

#UI with Gradio

with gr.Blocks() as demo:
    gr.Markdown("# Queens College CS Professor Reviews")
    gr.Markdown("Ask a question about Queens College CS professors and get an answer based on student reviews!")
    gr.Markdown("The Professors: ")
    gr.Markdown("Anne Smith Thompson, Delaram Kahrobaei, Paul Cesaretti, John Svadlenka, Mayank Goswami, Kent Boklan, Robert Goldberg, Matthew Fried, Simina Fluture, Russell Gomes")
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    btn.click(fn=handle_query, 
              inputs=inp, 
              outputs=answer
              )
    inp.submit(handle_query, 
               inputs=inp, 
               outputs=answer
               )

# Run the app
if __name__ == "__main__":
    print("\n" + "-"*50)
    print(" Queens College CS Professor Reviews — starting up")
    print("-"*50 + "\n")
    run_ingestion()
    demo.launch()
    
