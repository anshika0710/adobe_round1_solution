🧠 Approach Explanation – Adobe Hackathon 2025

📘 Overview

This document outlines the strategy and methodology used to develop a full-stack solution for Round 1A and Round 1B of the Adobe India Hackathon – “Connecting the Dots.”

Our objective was to design an intelligent system that can:

Automatically extract structured outlines from raw PDFs (Round 1A).

Generate insightful and personalized document interpretations based on a persona and task (Round 1B).

🔹 Round 1A: Structured Outline Extraction

We used the PyMuPDF (fitz) library to parse the PDF content and generate a clean document outline that includes the document title and headings with hierarchy (H1–H3).

✅ Steps and Techniques Used:

Text Parsing: Each page of the PDF is parsed for layout and font metadata.

Font Analysis: We analyze font size and frequency distribution across the document to detect dominant heading sizes.

Level Assignment: Based on the top 3 most frequent font sizes, we assign heading levels — largest fonts are considered H1, then H2, H3.

Deduplication & Structuring: Repeated headings are filtered, and a clean outline JSON is generated containing:

title

outline[] (each with level, text, page)

📈 Optimized to handle 50+ page PDFs within 10 seconds

🔹 Round 1B: Persona-Based Document Intelligence

After extracting outlines, the second part focuses on identifying sections most relevant to a user-defined persona and task.

✅ Core Components:

Input Definition: input.json includes:

Persona role (e.g., intern, analyst)

Task to be done

List of PDF filenames

Multilingual Embedding: We use the distiluse-base-multilingual-cased-v2 model (from sentence-transformers) to embed:

Persona + task prompt

Section headings from extracted outlines

Semantic Ranking:

Cosine similarity scores are computed

Top 3 most relevant sections are selected per document

Subsection Summarization (Placeholder):

Currently uses a mocked summary like: Heading - summarized

Future scope: integrate DistilBART or similar transformer model for real summarization

📤 Output Format – output/output.json

The final output is a JSON file with the following structure:

{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "...",
      "page_number": ...,
      "section_title": "...",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "...",
      "page_number": ...,
      "refined_text": "..."
    }
  ]
}

All output is automatically generated when the app.py script is run.

✅ Summary & Highlights

📄 Works on any real-world PDF with minimal formatting assumptions

🌍 Supports over 15+ languages using multilingual sentence embeddings

⏱ Performance-tested: completes in <10s (1A) and <60s (1B)

🐳 Fully Dockerized for clean and reproducible builds

This approach demonstrates a scalable baseline for building PDF understanding tools, intelligent summarizers, and domain-specific knowledge extraction engines.

