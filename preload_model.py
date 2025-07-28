from sentence_transformers import SentenceTransformer

# Load and cache the multilingual model
model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
print("✅ Model loaded and cached successfully!")
