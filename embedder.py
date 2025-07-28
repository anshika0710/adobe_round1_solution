from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import os

# Load embedding model
model = SentenceTransformer("distiluse-base-multilingual-cased-v2")


# Load summarizer model (cached offline)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

# Optional: Model size debug check
def get_model_size(model_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(model_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)

model_dir = os.path.expanduser("~/.cache")
print(f"📦 Model size (cached): {get_model_size(model_dir):.2f} MB")

# Summarize extracted text
def summarize_text(text):
    if len(text.split()) < 30:
        return text
    try:
        summary = summarizer(text, max_length=80, min_length=20, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return text

# Main embedding-based section ranking
def get_relevant_sections(sections, persona, job, top_k=5):
    query = f"{persona} needs to {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    section_texts = [s["text"] for s in sections]
    section_embeddings = model.encode(section_texts, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, section_embeddings)[0]
    results = sorted(zip(sections, similarities), key=lambda x: x[1], reverse=True)[:top_k]

    ranked_sections = []
    for rank, (section, score) in enumerate(results, 1):
        ranked_sections.append({
            "document": section["document"],
            "page_number": section["page"],
            "section_title": section["heading"],
            "importance_rank": rank,
            "refined_text": summarize_text(section["text"])
        })

    return ranked_sections
