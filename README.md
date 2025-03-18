# 📝 **Flask Cover Letter Generator**

This is a Flask-based API that extracts resume details from a PDF file and generates a professional cover letter using GPT-4o. The API extracts key information like name, experience, and skills from the resume and crafts a tailored cover letter in PDF format.

---

## 🚀 **How to Run**

### 1. **Create a Virtual Environment**

Create a virtual environment to isolate dependencies:

```bash
python -m venv venv
```

---

### 2. **Activate the Virtual Environment**

**Windows:**

```bash
.\venv\Scripts\activate
```

**MacOS/Linux:**

```bash
source venv/bin/activate
```

---

### 3. **Install Requirements**

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

### 4. **Create `.env` File**

Create a `.env` file in the root directory and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=sk-proj-...
```

---

### 5. **Run the App**

Start the Flask app:

```bash
python app.py
```

---

### ✅ **Python Version**

This project runs on **Python 3.12.7**

---

## 📌 **API Endpoints**

### ➡️ **Generate Cover Letter**

**Endpoint:**

```http
POST /generate_cover_letter
```

**Description:**

Generates a professional cover letter based on extracted resume data.

**Headers:**

| Key           | Value        | Required |
| ------------- | ------------ | -------- |
| `HR`        | HR's Name    | ✅       |
| `Job-Title` | Job Title    | ✅       |
| `Company`   | Company Name | ✅       |

**Body:**

| Key      | Type       | Description               | Required |
| -------- | ---------- | ------------------------- | -------- |
| `file` | File (PDF) | Resume file in PDF format | ✅       |

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:5000/generate_cover_letter" \
-H "HR: John Doe" \
-H "Job-Title: Software Engineer" \
-H "Company: OpenAI" \
-F "file=@resume.pdf"
```

**Example Request (Postman):**

1. Select `POST` method.
2. Enter URL: `http://127.0.0.1:5000/generate_cover_letter`
3. Add headers:
   * `HR: John Doe`
   * `Job-Title: Software Engineer`
   * `Company: OpenAI`
4. In `Body`, select **form-data** and upload the PDF file under the key  **file** .
5. Click  **Send** .

---

### ✅ **Successful Response**

Returns the generated cover letter as a downloadable PDF:

```json
{
    "filename": "cover_letter.pdf"
}
```

---

### ❌ **Error Response**

| Status Code | Error                                 | Description                         |
| ----------- | ------------------------------------- | ----------------------------------- |
| `400`     | `Missing HR, Job Title, or Company` | Missing required headers.           |
| `400`     | `No file provided`                  | File not uploaded in the request.   |
| `400`     | `No file selected`                  | No file selected during the upload. |
| `500`     | `Internal Server Error`             | Unexpected error occurred.          |

---
