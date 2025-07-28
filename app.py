import json, os
import time
from datetime import datetime
from extractor import extract_outline
from embedder import get_relevant_sections

# Start timer
start_time = time.time()

# Load config from input.json
with open("input/input.json", "r", encoding="utf-8") as f:
    config = json.load(f)

persona = config["persona"]["role"]
job = config["job_to_be_done"]["task"]
pdf_files = [doc["filename"] for doc in config["documents"]]

all_extracted_sections = []
all_subsection_summaries = []

# Process each PDF
for pdf in pdf_files:
    input_path = os.path.join("input", pdf)
    outline = extract_outline(input_path)

    # Prepare input for ML model
    sections_for_model = [
        {
            "document": pdf,
            "page": h["page"],
            "heading": h["text"],
            "text": h["text"]
        } for h in outline["outline"]
    ]

    ranked_sections = get_relevant_sections(sections_for_model, persona, job)

    for section in ranked_sections:
        extracted = {
            "document": section["document"],
            "page_number": section["page_number"],
            "section_title": section["section_title"],
            "importance_rank": section["importance_rank"]
        }
        all_extracted_sections.append(extracted)

        summary = {
            "document": section["document"],
            "page_number": section["page_number"],
            "refined_text": section["refined_text"]
        }
        all_subsection_summaries.append(summary)

# Final combined output
final_output = {
    "metadata": {
        "input_documents": pdf_files,
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.now().isoformat()
    },
    "extracted_sections": all_extracted_sections,
    "subsection_analysis": all_subsection_summaries
}

# Write to JSON
os.makedirs("output", exist_ok=True)
with open("output/output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

end_time = time.time()
print("✅ Combined output saved to output/output.json")
print(f"⏱️ Execution Time (1B): {end_time - start_time:.2f} seconds")

