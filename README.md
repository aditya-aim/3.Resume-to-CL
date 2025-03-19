# 📄 **Cover Letter Generator API**

This project provides a Flask-based API that allows users to generate professional cover letters based on resume data extracted from a PDF file using OpenAI's GPT model. The generated cover letter can be downloaded as a PDF or sent via email.

---

## 🚀 **Features**

* ✅ Upload a PDF resume
* ✅ Extract data using OpenAI GPT-4o
* ✅ Generate a custom cover letter based on extracted data
* ✅ Save the cover letter as a PDF
* ✅ Send the cover letter via email



---



### ✅ **Python Version**

This project runs on **Python 3.12.7**

## 📚 **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/cover-letter-generator.git
cd cover-letter-generator
```

### **2. Set Up a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Create a `.env` File**

Create a `.env` file in the project directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key
```

### **5. Start the Flask Server**

```bash
flask run
```

---

## 🛠️ **API Endpoints**

### **1. Generate Cover Letter**

Generates a cover letter based on data extracted from a resume PDF.

**URL:**

```
POST /generate_cover_letter
```

**Headers:**

| Header              | Type   | Required | Description                                      |
| ------------------- | ------ | -------- | ------------------------------------------------ |
| `HR`              | String | ✅       | Name of the HR or recruiter                      |
| `Job-Title`       | String | ✅       | Job title being applied for                      |
| `Company`         | String | ✅       | Company name                                     |
| `Job-Description` | String | ✅       | Description of the job                           |
| `Tone`            | String | ❌       | Writing tone (`Professional`,`Casual`, etc.) |
| `Style`           | String | ❌       | Writing style (`Concise`,`Detailed`, etc.)   |

**Request:**

* **Form-data:**
  * `file` → PDF file of the resume

**Example Request (cURL):**

```bash
curl -X POST http://127.0.0.1:5000/generate_cover_letter \
  -H "HR: John Doe" \
  -H "Job-Title: Software Engineer" \
  -H "Company: OpenAI" \
  -H "Job-Description: Develop AI models to improve user experience" \
  -F "file=@resume.pdf"
```

**Response:**

* **Success:** Returns the generated cover letter PDF
* **Failure:** JSON error message

**Example Response:**

```json
{
  "error": "Missing HR, Job Title, Company, or Job Description in headers"
}
```

---

### **2. Send Cover Letter via Email**

Sends the generated cover letter to the specified email address.

**URL:**

```
POST /send_cover_letter
```

**Headers:**

| Header    | Type   | Required | Description             |
| --------- | ------ | -------- | ----------------------- |
| `Email` | String | ✅       | Recipient email address |

**Example Request (cURL):**

```bash
curl -X POST http://127.0.0.1:5000/send_cover_letter \
  -H "Email: example@gmail.com"
```

**Response:**

* **Success:** `{ "message": "Cover letter sent successfully!" }`
* **Failure:** JSON error message

**Example Response:**

```json
{
  "error": "Cover letter not found. Generate it first."
}
```

---

## 🧠 **How It Works**

1. **Resume Upload:** The user uploads a PDF resume.
2. **Data Extraction:** OpenAI GPT-4o extracts key details like name, experience, and skills.
3. **Cover Letter Generation:** OpenAI generates a customized cover letter.
4. **PDF Generation:** The cover letter is saved as a PDF.
5. **Email Sending:** The cover letter can be sent via email.
