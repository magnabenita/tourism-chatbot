
import os, pickle, faiss
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use same multilingual model
model = SentenceTransformer("all-MiniLM-L6-v2")

base_path = os.path.dirname(__file__)

# Load combined index and data
index = faiss.read_index(os.path.join(base_path, "tourism_all_index.faiss"))
with open(os.path.join(base_path, "tourism_all_data.pkl"), "rb") as f:
    data = pickle.load(f)

class Query(BaseModel):
    query: str

@app.post("/query")
async def get_answer(q: Query):
    try:
        query_embedding = model.encode([q.query])
        D, I = index.search(query_embedding, k=1)
        best_match = data[I[0][0]]
        return {
            "answer": best_match["answer"],
            "language": best_match["lang"]
        }
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "language": None}
