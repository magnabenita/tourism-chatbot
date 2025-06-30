from fastapi import FastAPI
from pydantic import BaseModel
import json
from fuzzywuzzy import fuzz

app = FastAPI()

# Load English and Tamil datasets
with open("full_tamil_nadu_tourism_qa.json", "r", encoding="utf-8") as f:
    english_data = json.load(f)["tourism_questions_tamil_nadu"]

with open("tamil_tourism_qa_full.json", "r", encoding="utf-8") as f:
    tamil_data = json.load(f)["tourism_questions_tamil_nadu"]

class Query(BaseModel):
    query: str
    lang: str  # "en" or "ta"

@app.post("/query")
async def get_answer(q: Query):
    try:
        data = english_data if q.lang == "en" else tamil_data

        best_match = None
        best_score = 0

        for item in data:
            score = fuzz.token_set_ratio(q.query.lower(), item["question"].lower())
            if score > best_score:
                best_score = score
                best_match = item

        # Threshold: only return if score is 70+
        if best_score >= 70:
            return {"answer": best_match["answer"]}

        return {"answer": "மன்னிக்கவும், உங்கள் கேள்விக்கு தொடர்புடைய தகவல் இல்லை." if q.lang == "ta" else "Sorry, I don't have relevant information yet."}

    except Exception as e:
        return {"answer": f"Error occurred: {str(e)}"}
