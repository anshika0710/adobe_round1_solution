import fitz  # PyMuPDF
import json
import os

pdf_path = os.path.join("input", "sample.pdf")  # Make sure file name is correct
doc = fitz.open(pdf_path)

title = ""
headings = []
font_size_counts = {}

# Step 1: Analyze font sizes
for page_num, page in enumerate(doc):
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    size = round(s["size"], 1)
                    if len(text) < 2: continue
                    font_size_counts[size] = font_size_counts.get(size, 0) + 1

# Step 2: Rank font sizes to assign heading levels
sorted_fonts = sorted(font_size_counts.keys(), reverse=True)
font_levels = {}
for i, size in enumerate(sorted_fonts[:4]):
    font_levels[size] = f"H{i+1}"

# Step 3: Parse headings and title
for page_num, page in enumerate(doc):
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    size = round(s["size"], 1)
                    if len(text) < 2: continue
                    if not title:
                        title = text
                    level = font_levels.get(size)
                    if level:
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

# Step 4: Create JSON
result = {
    "title": title,
    "outline": headings
}

# Save JSON
output_path = os.path.join("output", "sample.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ Done. Output saved to:", output_path)
