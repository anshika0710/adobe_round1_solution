import fitz  # PyMuPDF
import time
import json
import os

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    headings = []
    font_size_counts = {}

    # Step 1: Count font sizes across all pages
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        size = round(s["size"], 1)
                        if len(text) < 2:
                            continue
                        font_size_counts[size] = font_size_counts.get(size, 0) + 1

    # Step 2: Assign heading levels by font size (largest = H1)
    sorted_sizes = sorted(font_size_counts.keys(), reverse=True)
    font_levels = {}
    for i, size in enumerate(sorted_sizes[:3]):
        font_levels[size] = f"H{i+1}"

    # Step 3: Extract headings
    seen = set()
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_text = ""
                    sizes = []

                    for s in l["spans"]:
                        text = s["text"].strip()
                        size = round(s["size"], 1)
                        if len(text) < 1:
                            continue
                        line_text += text + " "
                        sizes.append(size)

                    line_text = line_text.strip()
                    if not line_text or line_text in seen:
                        continue

                    if sizes:
                        line_size = max(set(sizes), key=sizes.count)
                        level = font_levels.get(line_size)
                        if level:
                            if not title:
                                title = line_text
                            headings.append({
                                "level": level,
                                "text": line_text,
                                "page": page_num + 1
                            })
                            seen.add(line_text)

    return {
        "title": title,
        "outline": headings
    }

# === Entry point for testing or standalone run === #
if __name__ == "__main__":
    import_path = "input/sample.pdf"
    export_path = "output/sample.json"

    start_time = time.time()

    result = extract_outline(import_path)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    end_time = time.time()
    print(f"[✅] Extracted outline written to {export_path}")
    print(f"[⏱️] Execution Time: {end_time - start_time:.2f} seconds")
