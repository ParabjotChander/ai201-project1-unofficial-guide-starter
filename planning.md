# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I choose student reviews of Computer Science Professors at CUNY Queens College. Each txt file shows reviews for an specific professor teaching, a total of 10 professors' reviews. This knowlegde will be valuable for students when they signup for classes for next semester, what professors should they have and which ones should they avoid. This information was hard to find through offical channels since the colleges' official website doesn't have professor reviews that are specific but more of a broad praise of them. 
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Paul Cesaretti.txt|Paul Cesaretti's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/2354095>
| 2 |Russell Gomes.txt|Russell Gomes's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/2913678> 
| 3 |Simina Fluture.txt|Simina Fluture's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/513427>
| 4 |Mayank Goswami.txt|Mayank Goswami's rate my professor reviews | | <https://www.ratemyprofessors.com/professor/2195317> 
| 5 |Anne Smith Thompson.txt|Anne Smith Thompson's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/352320> 
| 6 |John Svadlenka.txt|John Svadlenka's rate my professor reviews | | <https://www.ratemyprofessors.com/professor/2485140>
| 7 |Kent Boklan.txt|Kent Boklan's rate my professor reviews | | <https://www.ratemyprofessors.com/professor/629756>
| 8 |Delaram Kahrobaei.txt|Delaram Kahrobaei's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/2870283> 
| 9 |Matthew Fried.txt|Matthew Fried's rate my professor reviews | |<https://www.ratemyprofessors.com/professor/1822595>
| 10 |Robert Goldberg.txt|Robert Goldberg's rate my professor reviews | | <https://www.ratemyprofessors.com/professor/446485> 

---

## Chunking Strategy: Fixed Size

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 50 characters

**Overlap:** 10 characters

**Reasoning:** 
I will split my documents by character count, fixed size since my files contain reviews of professors which aren't too long, each review for a professor is a brief paragraph. To prevent the cutting of words, I will use an overlap. The benefits of this approach is that it is simple, fast, predictable and no Natural Language Processing is needed. It's good for uniform short documents (reviews)
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers python AI library

**Top-k:** I am aiming to recieve between 100 to 200 chunks!

**Production tradeoff reflection:**
If I was deploying this for real users and cost wasn't a constraint, I would look into vector length, higher dimensional vectors (vectors with more numbers in them) will have better embedding matchs but at a high cost and more latency. I would be interesting to consider if my embedding model could capture more tokens. 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |For Delaram Kahrobaei as a professor, you can understand the concepts through what? | Review Sheet |
| 2 |How many questions are in Matthew Fried's test and many minutes you have to complete them? | 65 questions and 50 minutes roughly |
| 3 |What are the submission steps for a singe file for Robert Goldberg? | 10 step nightmare of manual work |
| 4 |Can you describe Simina Fluture's assigments and exams?| vague with unsure expectations|
| 5 |What are the ways to pass Kent Boklan's class? | attend every class and showing up to the office hours|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. If my overlap character count is too low, can get cut off answers with no context. I know I am going to have to fine tune the character split and overlap count to where the chunks are just big enough to answer and just small enough to be precise.

2. The model doesn't use chunks to retrieve the answer but uses training data, using memory rather than the documents. To prevent this, I will give strong grounding questions to the LLM, telling it explicitly not to draw outside knowledge.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
   ![RAG Pipeline Diagram](<RAG Pipeline Diagram.png>)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
                I'll use the class lab for reference and guidance in terms of the document loading, I have text files.
                I'll give Claude my Chunking Strategy section (fixed size) and ask it to implement chunk_text() method with my specified chunk size and overlap.

**Milestone 4 — Embedding and retrieval:**
                I will have have to store the chunks in the embed_and_store() method! 
                I'll ask AI for an guide on Python's sentence-transformers usage.

**Milestone 5 — Generation and interface:**
                I'll will tell Claude by grounding instructions for generation in the generate_reponse() method
                Do some research on Gradio python library before creating simple UI which displays a text box to display the query and the response. 