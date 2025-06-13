
# RAG QA Assistant

## 🛠️ Setup Instructions

### 1. Clone or Unzip

```bash
git clone <your-repo-url>
cd <project-folder>
```

> Or unzip the `.zip` and navigate into the folder.

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `.env` file

Inside the project folder, create a file named `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 4. (Optional) Add Research Papers

- Create a folder named `papers/` and add your `.pdf` files  
- **OR** use the file upload option directly from the Streamlit UI

---

### 5. Run the App

```bash
streamlit run main.py
```

---

## 📌 Notes

- PDFs and `.env` are excluded from the repo using `.gitignore`
- Supports both file upload and local directory methods
- Make sure you have internet access for model loading and Gemini API

---

## 📦 Requirements

- Python 3.8+
- See `requirements.txt` for full list

---
