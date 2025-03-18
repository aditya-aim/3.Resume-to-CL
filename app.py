import os
from flask import Flask, request, send_file, jsonify
import fitz  # PyMuPDF
import openai
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

app = Flask(__name__)
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


client = openai.Client(api_key=api_key)

def extract_resume_data(resume_text):
    prompt = f"""
    Extract the following information from the resume:
    - Full Name
    - Experience 
    - Key Skills (comma-separated)

    Resume:
    {resume_text}

    Format:
    - Name: <Name>
    - Experience: <Experience>
    - Skills: <Skills>
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    extracted_data = response.choices[0].message.content.strip().split("\n")
    
    print("\n[Raw Extracted Data]:", extracted_data)

    data = {}
    for item in extracted_data:
        if ": " in item:
            key, value = item.split(": ", 1)
            data[key.strip('- ').strip()] = value.strip()
        else:
            print(f"Skipping malformed line: {item}")

    return data

def generate_cover_letter(name, job_title, company, experience, skills, job_description, HR):
    prompt = f"""
    Write a professional cover letter for {name} applying for the position of {job_title} at {company}.
    - Mention relevant experience: {experience}
    - Include key skills: {skills}
    - Job description: {job_description}
    - It is being written to: {HR}
    - Format the output strictly in the following format:
    
    {name}  
    Bengaluru  |  +91-9454441867  |  adityasagarverma@gmail.com  
    <newline>  
    <newline>  
    Dear {HR},  
    <newline>  
    <INTRODUCTION_PARAGRAPH>  
    <newline>  
    <EXPERIENCE_PARAGRAPH>  
    <newline>  
    <SKILLS_PARAGRAPH>  
    <newline>  
    <MOTIVATION_PARAGRAPH>  
    <newline>  
    Warmest regards,  
    {name}  

    - Ensure that placeholders like `<INTRODUCTION_PARAGRAPH>`, `<EXPERIENCE_PARAGRAPH>`, etc., are properly filled in based on the job description and other details.
    - Maintain consistent use of `<newline>` to separate paragraphs.
    - Follow a professional and concise tone.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

def parse_pdf(pdf_path):
    # Read PDF content using PyMuPDF
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text



import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Function to save PDF in the current directory
def save_cover_letter_as_pdf(content, filename="cover_letter.pdf"):
    pdf_file_path = os.path.join(os.getcwd(), filename)

    # Set up the PDF document
    doc = SimpleDocTemplate(
        pdf_file_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        spaceAfter=5,
        alignment=1,  # Center alignment
        textColor=colors.black
    )

    subheader_style = ParagraphStyle(
        'Subheader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=14,
        spaceAfter=5,
        alignment=1,  # Center alignment
        textColor=colors.black
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=13,
        spaceAfter=5,
        alignment=0,  # Left alignment
    )

    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        spaceAfter=2,
        alignment=0,
    )

    italic_style = ParagraphStyle(
        'Italic',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=13,
        spaceAfter=2,
        alignment=0,
    )

    bold_italic_style = ParagraphStyle(
        'BoldItalic',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=11,
        leading=13,
        spaceAfter=2,
        alignment=0,
    )

    # Split content into paragraphs and apply formatting
    flowables = []

    # First line → Header
    lines = content.strip().split("\n")
    if lines:
        flowables.append(Paragraph(lines[0], header_style))

    # Second line → Subheader (contact details)
    if len(lines) > 1:
        flowables.append(Paragraph(lines[1], subheader_style))

    # Add a blank line after header and subheader
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(Spacer(1, 0.2 * inch))

    # Process the rest of the content
    for line in lines[2:]:
        line = line.strip()

        if line == "<newline>":
            flowables.append(Spacer(1, 0.2 * inch))  # Add blank line
        elif line.startswith("***") and line.endswith("***"):
            flowables.append(Paragraph(line[3:-3], bold_italic_style))
        elif line.startswith("**") and line.endswith("**"):
            flowables.append(Paragraph(line[2:-2], bold_style))
        elif line.startswith("*") and line.endswith("*"):
            flowables.append(Paragraph(line[1:-1], italic_style))
        elif line:
            flowables.append(Paragraph(line, body_style))

    # Build the PDF
    doc.build(flowables)
    return pdf_file_path



#============================================ API ==========================================

# ------------ Flask Route ----------------
@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter_api():
    try:
        # Receive headers
        hr = request.headers.get('HR')
        job_title = request.headers.get('Job-Title')
        company = request.headers.get('Company')
        job_description = request.headers.get('Job-Description')

        if not hr or not job_title or not company or not job_description:
            return jsonify({"error": "Missing HR, Job Title, Company, or Job Description in headers"}), 400
        
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided or file name is empty"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save uploaded file
        file_path = os.path.join(os.getcwd(), file.filename)
        file.save(file_path)

        # Step 1: Extract text from PDF
        resume_text = parse_pdf(file_path)
        
        # Step 2: Extract data using LLM
        extracted_data = extract_resume_data(resume_text)
        print("\n[Extracted Data]:", extracted_data)

        # Step 3: Generate Cover Letter
        cover_letter = generate_cover_letter(
            extracted_data["Name"],
            job_title,
            company,
            extracted_data["Experience"],
            extracted_data["Skills"],
            job_description,
            hr
        )

        # Step 4: Save Cover Letter as PDF
        pdf_path = save_cover_letter_as_pdf(cover_letter)

        # Step 5: Send PDF as response
        return send_file(pdf_path, as_attachment=True, download_name="cover_letter.pdf")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------ Main ----------------
if __name__ == "__main__":
    app.run(debug=True)
