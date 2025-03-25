# 📄 **Cover Letter Generator API**

A Flask-based API that generates professional cover letters from PDF resumes using OpenAI's GPT model. The API supports PDF generation and email delivery of cover letters.

## 📁 **Project Structure**

```
cover-letter-generator/
├── app.py                 # Main Flask application with API endpoints
├── templates/             # Frontend templates
│   └── index.html        # Main web interface
├── .env                  # Environment variables (API keys, credentials)
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## 🔑 **Environment Variables**

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your-openai-api-key
FLASK_SECRET_KEY=your-secret-key-here
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-email-app-password
```

## 📚 **API Documentation**

### Base URL

```
http://localhost:5000
```

### Endpoints

#### 1. Upload Resume

```http
POST /upload
Content-Type: multipart/form-data

Form Data:
- resume: PDF file
```

**Response (200 OK)**

```json
{
    "message": "Resume processed successfully",
    "data": {
        "name": "Extracted Name",
        "experience": "Years of Experience",
        "skills": "Comma-separated Skills"
    }
}
```

**Error Responses**

- 400 Bad Request: No file provided or invalid file type
- 500 Internal Server Error: Processing failure

#### 2. Generate Cover Letter

```http
POST /generate_cover_letter
Content-Type: multipart/form-data

Form Data:
- job_title: string
- company: string
- job_description: string
- hr_name: string (optional, default: "Hiring Manager")
- name: string (optional, from resume)
- experience: string (optional, from resume)
- skills: string (optional, from resume)
- introduction_weight: integer (1-5, default: 3)
- experience_weight: integer (1-5, default: 3)
- skills_weight: integer (1-5, default: 3)
- motivation_weight: integer (1-5, default: 3)
- conclusion_weight: integer (1-5, default: 3)
```

**Response (200 OK)**

```json
{
    "message": "Cover letter generated successfully",
    "pdf_path": "path/to/cover_letter.pdf"
}
```

**Error Responses**

- 400 Bad Request: Missing required fields
- 500 Internal Server Error: Generation failure

#### 3. Download Cover Letter

```http
GET /download_cover_letter
```

**Response (200 OK)**

- Content-Type: application/pdf
- File: cover_letter.pdf

**Error Responses**

- 404 Not Found: Cover letter not generated
- 500 Internal Server Error: Download failure

#### 4. Send Cover Letter via Email

```http
POST /send_cover_letter
Content-Type: multipart/form-data

Form Data:
- email: string (recipient email)
```

**Response (200 OK)**

```json
{
    "message": "Cover letter sent successfully"
}
```

**Error Responses**

- 400 Bad Request: No email provided
- 404 Not Found: Cover letter not generated
- 500 Internal Server Error: Email sending failure

## 🛠️ **Setup & Installation**

1. **Clone Repository**

```bash
git clone https://github.com/your-repo/cover-letter-generator.git
cd cover-letter-generator
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Application**

```bash
flask run
```

## ⚠️ **Error Handling**

All endpoints return appropriate HTTP status codes and JSON error messages:

```json
{
    "error": "Error message description"
}
```

Common status codes:

- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error
