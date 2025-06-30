# Deep-Shiva Tourism Chatbot (Backend)
# 🧭 Tamil Nadu Tourism Chatbot (Stage 1 Prototype)

This is a backend prototype for a domain-specific multilingual chatbot built for the **Deep-Shiva National Chatbot Hackathon**, focused on Tamil Nadu tourism.

It supports question-answering about popular heritage sites, cultural practices, travel tips, and more — in both **English** and **Tamil**.

---

## 🌐 Features

- ✅ FastAPI backend with `/query` endpoint
- ✅ Semantic search using Sentence Transformers
- ✅ FAISS vector database for fast retrieval
- ✅ Supports English and Tamil queries
- ✅ No keyword matching — true semantic understanding

---


## 📁 Project Structure
deepshiva-tourism-chatbot/
├── backend/
│ ├── backend.py # FastAPI app
│ ├── build_index.py # Script to build FAISS index
│ ├── full_tamil_nadu_tourism_qa.json # English Q&A data
│ ├── tamil_tourism_qa_full.json # Tamil Q&A data
│ ├── tourism_all_data.pkl # Pickled Q&A (generated)
│ ├── tourism_all_index.faiss # FAISS index file (generated)
├── requirements.txt
├── README.md


## How to Run
```bash
pip install -r requirements.txt
python backend/build_index.py
```
This will generate:
    *tourism_all_data.pkl
    *tourism_all_index.faiss

```bash
uvicorn backend.backend:app --reload
```
