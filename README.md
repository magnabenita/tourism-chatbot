# Deep-Shiva Tourism Chatbot (Backend)

This is the backend for a domain-specific chatbot focused on Tamil Nadu tourism, built for the Deep-Shiva competition.

## Features
- FastAPI backend
- Fuzzy matching Q&A using JSON dataset
- Multilingual support (English + Tamil)

## How to Run
```bash
pip install -r requirements.txt
uvicorn backend.backend:app --reload
