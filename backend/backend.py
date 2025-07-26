import os, pickle, faiss
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory path
base_path = os.path.dirname(__file__)

# Lazy loading model, index, and data
model = None
index = None
data = None

def load_resources():
    global model, index, data
    if model is None:
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    if index is None:
        index_path = os.path.join(base_path, "tourism_all_index.faiss")
        index = faiss.read_index(index_path)
    if data is None:
        with open(os.path.join(base_path, "tourism_all_data.pkl"), "rb") as f:
            data = pickle.load(f)

# Input schema
class Query(BaseModel):
    query: str

# Endpoint
@app.post("/query")
async def get_answer(q: Query):
    try:
        load_resources()
        query_embedding = model.encode([q.query])
        D, I = index.search(query_embedding, k=1)
        best_match = data[I[0][0]]
        return {
            "answer": best_match["answer"],
            "language": best_match["lang"]
        }
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "language": None}
