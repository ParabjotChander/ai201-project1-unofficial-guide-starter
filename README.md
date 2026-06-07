# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I compiled and analyzed student reviews for 10 Computer Science professors at CUNY Queens College, with data structured into individual text files per instructor. The goal of this project is to provide students with actionable insights ahead of semester registration, helping them identify which professors best align with their learning styles. This granular data fills a major gap in official university resources, which often lean toward broad promotional praise rather than specific, professor-level feedback.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->


| # | Source | Type | URL or location |
|---|--------|-------------|-----------------|
| 1 |Paul Cesaretti.txt| Text File | /documents/Paul Cesaretti.txt |
| 2 |Russell Gomes.txt|Text File | /documents/Russell Gomes.txt |
| 3 |Simina Fluture.txt|Text File | /documents/Simina Fluture.txt |
| 4 |Mayank Goswami.txt|Text File | /documents/Mayank Goswami.txt | 
| 5 |Anne Smith Thompson.txt|Text File | /documents/Anne Smith Thompson.txt|
| 6 |John Svadlenka.txt|Text File | /documents/John Svadlenka.txt | 
| 7 |Kent Boklan.txt|Text File | /documents/Kent Boklan.txt | 
| 8 |Delaram Kahrobaei.txt|Text File | /documents/Delaram Kahrobaei.txt |
| 9 |Matthew Fried.txt|Text File | /documents/Matthew Fried.txt |
| 10 |Robert Goldberg.txt|Text File | /documents/Robert Goldberg.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 250 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**
I choose Fixed Size Chunking since the documents or files were of professor reviews, each review was an brief paragraph. This chunking strategy is good for short uniform documents. I added an overlap so that retrieved chunks wouldn't have cut across sentences, ideas and no awareness of the context. In terms of preprocessing, web scraping on the Rate My Professor was a nightmare, I had to manually add the (5-6) reviews each txt file as it mentioned in the project directions that I might have to do that.

**Final chunk count:** 101

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers Python API Library

**Production tradeoff reflection:**
If I was deploying this for real users and cost wasn't a constraint I would upgrade to a high-dimensional embedding model (more numbers representing a chunk, bigger vector length) to increase retrieval accuracy. Since cost isn't a factor, I would host the model on an API rather than local, local hosting on consumer hardware can introduce latency. I would consider using multilingual support so users from different languagesand backgrounds (other than English) can use it. 

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
My system prompt groudning instructions were telling the LLM to cite the source in the prompt, and not make up the response but use only the retrieved chunks to generate the response and if you don't know the answer say you don't know. 

     "Use only the following retrieved rule chunks as context for your answer and cite the source. "
     "If the answer isn't in the chunks, say you don't know instead of making something up."
                
**How source attribution is surfaced in the response:**
I formatted the context chunks by providing the chunked text followed by the professor that text came from, so this way, the LLM will know the sources of the retrieved chunks when it generates the prompt and provide them in it.

format_chunks = lambda chunks: "\n\n".join(
    [f"{c['text']} (from {c['professor']})" for c in chunks]
)

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |How many questions are in Matthew Fried's test and how many minutes you have to complete them?|65 questions and 50 minutes roughly|According to the context from Matthew Fried, there are 65 questions in his tests and you have roughly 50 minutes to complete them. (Source: Matthew Fried Rate My Professor Reviews)|Good|Good|
| 2 |For Delaram Kahrobaei as a professor, you can understand the concepts through what? |Review Sheet|For Delaram Kahrobaei as a professor, you can understand the concepts through the review sheet. (Source: Delaram Kahrobaei Rate My Professor Reviews)|Good|Good|
| 3 |What are the submission steps for a singe file for Robert Goldberg?|10 step nightmare of manual work|According to Robert Goldberg, the submission steps for a single file are "a 10 step nightmare of manual work" (Source: Robert Goldberg).|Good|Good|
| 4 |Can you describe Simina Fluture's assigments and exams?|vague with unsure expectations|According to the context, Simina Fluture's class has "no homework and only 2/3 exams for the entire semester" (Source: Simina Fluture reviews). This suggests that her assignments are limited, with no homework, and the class has a relatively small number of exams.|Okay|Partially Accurate|
| 5 |What are the ways to pass Kent Boklan's class? |attend every class and showing up to the office hours|According to the context, the ways to pass Kent Boklan's class are: 1. Attending every single class (from Kent Boklan) 2. Showing up to his office hours (from Kent Boklan and Robert Goldberg) 3. Studying (from John Svadlenka) Note that Robert Goldberg also mentions spamming random questions during office hours, but it's not explicitly stated as a requirement to pass the class. (Source: Kent Boklan, Robert Goldberg, and John Svadlenka's reviews) |Bad|Partially Accurate|

**Retrieval quality:** Partially relevant
**Response accuracy:** Partially accurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Can you describe Simina Fluture's assigments and exams?
What are the ways to pass Kent Boklan's class?

**What the system returned:**
For Simina Fluture's question, the last sentence is not necessary, its jargon from the LLM.
For Kent Boklan's question, the first 2 numbered bullet points are correct, the rest is wrong and addresses other professor reviews. It uses 3 sources to answer the query when it should only use Kent Boklan.txt, not Robert Goldberg and John Svadlenka.

**Root cause (tied to a specific pipeline stage):**
For Simina Fluture's question, the LLM gives an confidence answer in the last sentence (generation stage).
For Kent Boklan's question, the retrieved chunks have a distance score from 0.4 to 0.6 (retrieval stage).

**What you would change to fix it:**
For Simina Fluture's question, I will have to change the LLM hard grounding isntructions, making them more clear. 
For Kent Boklan's question, I may have to consider changing the chunk and overlap size, fine tune the parameters and add distance score filtering, keeping the lower distances only.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Planning MD file helped me shape my implementation by breaking the project into smaller pieces, on each stage I knew what to do in each python file. For example, in the ingest.py file, I knew this is where the document loading and chunking strategy methods needed to be implemented. I had to decide what chunking strategy to use by writing it in the MD file. So when I used AI, the prompts were specific and not vague.

**One way your implementation diverged from the spec, and why:**
I intially had a low chunk and overlap size, as I retrieved chunks that were intially too large, so I had to change the parameters for my chunking mehtod. Throughout the project I changed my planning MD file quite a lot.  
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
Claude
I have text files.want to implement character fixed chunking of 100 characters with an overlap of 20 characters. I loaded the data already with my loaded_documents variable, which is a list where each element is a dictionary. The dictionary elements consist of this format. The text in the dictionary is the actual text from the doc.

     {
     "professor": professor_name,
     "filename": filename,
     "text": text
     }
     I have created a method called chunk_text() NOTE: I changed the chunking and overlap size to 250 and 50 characters respectively

- *What it produced:*
chunked_documents = []

for doc in loaded_documents:
    chunks = chunk_text(doc["text"], chunk_size=100, overlap=20)
    for i, chunk in enumerate(chunks):
        chunked_documents.append({
            "professor": doc["professor"],
            "filename": doc["filename"],
            "chunk_index": i,
            "text": chunk
        })

- *What I changed or overrode:*
NOTE: I changed the chunking and overlap size to 250 and 50 characters respectively, the chunks generated intially were long, I fine tuned these parameters. 

**Instance 2**

- *What I gave the AI:*
ChatGPT 
I am giving you the following code 
def handle_query(message): 
     if not message.strip(): 
          return "Ask a question to get started!", 
          retrieved_chunks = retrieve(message) 
          return generate_response(message, retrieved_chunks) 

#UI with Gradio 
with gr.Blocks() as demo: 
inp = gr.Textbox(label="Your question") 
btn = gr.Button("Ask") 
answer = gr.Textbox(label="Answer", lines=8) 
sources = gr.Textbox(label="Retrieved from", lines=4) 
btn.click(handle_query, inputs=message, outputs=handle_query) 
inp.submit(handle_query, inputs=inp, outputs=[answer, sources]). 
I know I am doing somthing wrong or am unsure,

- *What it produced:*
def handle_query(message):
    if not message.strip():
        return "Ask a question to get started!"

    retrieved_chunks = retrieve(message)
    return generate_response(message, retrieved_chunks)


with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your Question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)

    btn.click(
        fn=handle_query,
        inputs=inp,
        outputs=answer
    )

    inp.submit(
        fn=handle_query,
        inputs=inp,
        outputs=answer
    )

demo.launch()
- *What I changed or overrode:*
I added headers and paragraphs to improve the UI:
     gr.Markdown("# Queens College CS Professor Reviews")
     gr.Markdown("Ask a question about Queens College CS professors and get an answer based on student reviews!")
     gr.Markdown("The Professors: ")
     gr.Markdown("Anne Smith Thompson, Delaram Kahrobaei, Paul Cesaretti, John Svadlenka, Mayank Goswami, Kent Boklan, Robert Goldberg, Matthew Fried, Simina Fluture, Russell Gomes")

