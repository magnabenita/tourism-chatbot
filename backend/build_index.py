import os, json, pickle
import faiss
from sentence_transformers import SentenceTransformer

# Use a multilingual model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

base_path = os.path.dirname(__file__)

# Load English data
with open(os.path.join(base_path, "full_tamil_nadu_tourism_qa.json"), "r", encoding="utf-8") as f:
    en_data = json.load(f)["tourism_questions_tamil_nadu"]
    for item in en_data:
        item["lang"] = "en"

# Load Tamil data
with open(os.path.join(base_path, "tamil_tourism_qa_full.json"), "r", encoding="utf-8") as f:
    ta_data = json.load(f)["tourism_questions_tamil_nadu"]
    for item in ta_data:
        item["lang"] = "ta"

# Combine all
all_data = en_data + ta_data
questions = [item["question"] for item in all_data]

# Encode all questions
embeddings = model.encode(questions)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(embeddings)

# Save index and data
faiss.write_index(index, os.path.join(base_path, "tourism_all_index.faiss"))
with open(os.path.join(base_path, "tourism_all_data.pkl"), "wb") as f:
    pickle.dump(all_data, f)