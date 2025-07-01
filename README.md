# 🧭 DeepShiva - Domain-Specific Tourism Chatbot

A multilingual (English + Tamil) AI chatbot that answers tourism-related queries about Tamil Nadu using a custom Q&A dataset, semantic search with FAISS, and a beautiful Streamlit frontend.

---

## 🚀 Features

- 🔍 Intelligent tourism Q&A using semantic search (FAISS + Sentence Transformers)
- 🌐 Supports English & Tamil queries automatically
- 🧠 Backend powered by FastAPI + FAISS
- 💬 Frontend built with Streamlit
- 🖼️ Custom background image and chat UI
- 🗃️ Local embedding index for blazing-fast performance

---

## 📁 Project Structure

```
deepshiva-tourism-chatbot/
├── backend/
│   ├── backend.py                # FastAPI app
│   ├── build_index.py           # Embedding + FAISS index generator
│   ├── full_tamil_nadu_tourism_qa.json   # English QA dataset
│   ├── tamil_tourism_qa_full.json        # Tamil QA dataset
│   ├── tourism_index.faiss      # FAISS index (generated)
│   ├── tourism_data.pkl         # Raw data (generated)
│
├── frontend/
│   ├── app.py                   # Streamlit frontend
│   ├── Thanjai.jpg              # Background image
│
├── requirements.txt
├── .gitignore
├── README.md
```

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/tourism-chatbot.git
cd tourism-chatbot
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate        # On Windows
source venv/bin/activate     # On Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Backend Setup

### Step 1: Generate embeddings and FAISS index

```bash
cd backend
python build_index.py
```

> ✅ This creates:
> - `tourism_index.faiss`
> - `tourism_data.pkl`

### Step 2: Start the FastAPI backend

```bash
uvicorn backend:app --reload
```

You should see: `Running on http://127.0.0.1:8000`

---

## 💻 Frontend Setup

Open a **new terminal**:

```bash
cd frontend
streamlit run app.py
```

It should open a browser tab with the chatbot UI.

---

## 🌍 Language Detection

The app auto-detects Tamil characters (Unicode range) and routes to the correct dataset:

| Input Language | Dataset Used                |
|----------------|-----------------------------|
| English        | full_tamil_nadu_tourism_qa.json |
| Tamil          | tamil_tourism_qa_full.json      |

---

## 🧪 Example Questions

- **English:**  
  `What is the significance of the Meenakshi Temple in Madurai?`

- **Tamil:**  
  `மதுரையில் மீனாட்சியம்மன் கோயிலின் முக்கியத்துவம் என்ன?`

---

## 🧹 .gitignore

```gitignore
__pycache__/
*.pkl
*.faiss
venv/
.env
```