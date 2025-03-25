import os
from flask import Flask, request, send_file, jsonify, render_template, session
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
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here")  # Make sure to set FLASK_SECRET_KEY in your .env file
client = openai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

def extract_resume_data(resume_text):
    prompt = f"""
    Extract the following information from the resume,be careful user might have given dates,so calculate and give Experience accordingly:
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

def generate_cover_letter(name, job_title, company, experience, skills, job_description, HR, tone="Professional", style="Concise",
                          introduction_weight=1, experience_weight=1, skills_weight=1, motivation_weight=1, conclusion_weight=1):
    prompt = f"""
    Write a {tone.lower()} and {style.lower()} cover letter for {name} applying for the position of {job_title} at {company}.
    
    The importance of each section should be reflected in its length and detail:
    - Introduction section: {introduction_weight}/5 importance - Write {introduction_weight} sentences
    - Experience section: {experience_weight}/5 importance - Write {experience_weight} sentences
    - Skills section: {skills_weight}/5 importance - Write {skills_weight} sentences
    - Motivation section: {motivation_weight}/5 importance - Write {motivation_weight} sentences
    - Conclusion section: {conclusion_weight}/5 importance - Write {conclusion_weight} sentences
    
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
    <INTRODUCTION_PARAGRAPH> (Write {introduction_weight} sentences)  
    <newline>  
    <EXPERIENCE_PARAGRAPH> (Write {experience_weight} sentences)  
    <newline>  
    <SKILLS_PARAGRAPH> (Write {skills_weight} sentences)  
    <newline>  
    <MOTIVATION_PARAGRAPH> (Write {motivation_weight} sentences)  
    <newline>  
    <CONCLUSION_PARAGRAPH> (Write {conclusion_weight} sentences)  
    <newline>  
    Warmest regards,  
    {name}  
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

#------------------------------------- MAIL SEND
from flask import Flask, request, jsonify, send_file
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(receiver_email, pdf_path):
    sender_email = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    #receiver_email = os.getenv("RECEIVER_EMAIL")
 

    # Email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Your Personalized Cover Letter is Ready!"
    
    body = """Dear Candidate,

Your tailored cover letter has been generated successfully and is attached to this email.  
We hope it helps you make a strong impression.

Best regards,  
Machine-Hack💀
"""
    message.attach(MIMEText(body, 'plain'))
    
    # Attach the PDF file
    with open(pdf_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(pdf_path)}'
        )
        message.attach(part)
    
    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

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

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and file.filename.endswith('.pdf'):
            # Save the file with a unique name
            temp_path = os.path.join(os.getcwd(), 'temp_resume.pdf')
            file.save(temp_path)
            
            try:
                # Extract text from PDF
                resume_text = parse_pdf(temp_path)
                
                # Extract data from resume text
                extracted_data = extract_resume_data(resume_text)
                
                # Store the resume text in session for later use
                session['resume_text'] = resume_text
                
                return jsonify({
                    'message': 'Resume processed successfully',
                    'data': {
                        'name': extracted_data.get('Name', ''),
                        'experience': extracted_data.get('Experience', ''),
                        'skills': extracted_data.get('Skills', '')
                    }
                }), 200
                
            except Exception as e:
                # Clean up the temporary file in case of error
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise e
        
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
    
    except Exception as e:
        print(f"Error in upload_resume: {str(e)}")
        return jsonify({'error': 'Failed to process resume'}), 500

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter_route():
    try:
        # Get form data
        job_title = request.form.get('job_title')
        company = request.form.get('company')
        job_description = request.form.get('job_description')
        hr_name = request.form.get('hr_name', 'Hiring Manager')
        
        # Get the edited extracted information
        name = request.form.get('name')
        experience = request.form.get('experience')
        skills = request.form.get('skills')
        
        # Get the weights
        introduction_weight = int(request.form.get('introduction_weight', 3))
        experience_weight = int(request.form.get('experience_weight', 3))
        skills_weight = int(request.form.get('skills_weight', 3))
        motivation_weight = int(request.form.get('motivation_weight', 3))
        conclusion_weight = int(request.form.get('conclusion_weight', 3))
        
        # If edited values are not provided, use the extracted data from resume
        if not all([name, experience, skills]):
            # Get the resume text from session
            resume_text = session.get('resume_text')
            if not resume_text:
                return jsonify({'error': 'Please upload a resume first'}), 400
            
            # Extract data from resume
            resume_data = extract_resume_data(resume_text)
            name = name or resume_data.get('Name', '')
            experience = experience or resume_data.get('Experience', '')
            skills = skills or resume_data.get('Skills', '')
        
        # Generate cover letter
        cover_letter = generate_cover_letter(
            name=name,
            job_title=job_title,
            company=company,
            experience=experience,
            skills=skills,
            job_description=job_description,
            HR=hr_name,
            introduction_weight=introduction_weight,
            experience_weight=experience_weight,
            skills_weight=skills_weight,
            motivation_weight=motivation_weight,
            conclusion_weight=conclusion_weight
        )
        
        # Save as PDF
        pdf_path = save_cover_letter_as_pdf(cover_letter)
        
        return jsonify({
            'message': 'Cover letter generated successfully',
            'pdf_path': pdf_path
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_cover_letter', methods=['POST'])
def send_cover_letter():
    try:
        email = request.form.get('email')
        if not email:
            return jsonify({'error': 'No email provided'}), 400
        
        pdf_path = os.path.join(os.getcwd(), 'cover_letter.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'Cover letter not found'}), 404
        
        send_email(email, pdf_path)
        return jsonify({'message': 'Cover letter sent successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_cover_letter')
def download_cover_letter():
    try:
        pdf_path = os.path.join(os.getcwd(), 'cover_letter.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'Cover letter not found'}), 404
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='cover_letter.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
