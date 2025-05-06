from xhtml2pdf import pisa
from io import BytesIO

def generate_resume_from_parsed_data(parsed_data: dict) -> bytes:
    """
    Generate a resume PDF from parsed data using xhtml2pdf.
    """

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
                line-height: 1.4;
            }}
            h1 {{
                color: #4CAF50;
                text-align: center;
                margin-bottom: 10px;
                font-size: 30px;
            }}
            h2 {{
                color: #4CAF50;
                margin-top: 10px;
                margin-bottom: 5px;
                font-size: 24px;
            }}
            .contact-info {{
                text-align: center;
                margin-bottom: 20px;
                font-size: 16px;
            }}
            .contact-info p {{
                display: inline-block;
                margin-right: 20px;
                margin-bottom: 5px;
            }}
            .section {{
                margin-bottom: 15px;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 5px;
                padding-bottom: 2px;
                display: inline-block;
            }}
            .section-content {{
                margin-left: 20px;
                padding-left: 10px;
                margin-top: 3px;
                font-size: 14px;
            }}
            .item {{
                margin-bottom: 6px;
            }}
            .degree, .role, .certification {{
                font-weight: bold;
            }}
            .institution, .company {{
                font-style: italic;
            }}
            .list-item {{
                list-style-type: none;
            }}
            .skills-list {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                grid-gap: 10px;
                padding-left: 0;
                margin-top: 0;
            }}
            .skills-list li {{
                margin-bottom: 5px;
            }}
            .certifications-list, .interests-list {{
                padding-left: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>{parsed_data.get('name', 'Not Available')}</h1>
        <div class="contact-info">
            <p>Email: {parsed_data.get('email', 'Not Available')}</p>
            <p>Phone: {parsed_data.get('phone', 'Not Available')}</p>
        </div>
    """

    # Education Section
    education = parsed_data.get('education', [])
    html_content += "<div class='section'><div class='section-title'>Education</div><div class='section-content'>"
    if isinstance(education, list) and education:
        for item in education:
            html_content += f"""
            <div class="item">
                <span class="degree">{item.get('degree', 'Not Available')}</span><br>
                <span class="institution">{item.get('institution', 'Not Available')}</span> ({item.get('location', 'Not Available')})<br>
                CGPA: {item.get('cgpa', 'Not Available')}
            </div>
            """
    else:
        html_content += "<div class='item'>Not Available</div>"
    html_content += "</div></div>"

    # Skills Section
    skills = parsed_data.get('skills', [])
    html_content += "<div class='section'><div class='section-title'>Skills</div><div class='section-content'><ul class='skills-list'>"
    if isinstance(skills, list) and skills:
        for skill in skills:
            html_content += f"<li class='list-item'>{skill}</li>"
    else:
        html_content += "<li class='list-item'>Not Available</li>"
    html_content += "</ul></div></div>"

    # Experience Section
    experience = parsed_data.get('experience', [])
    html_content += "<div class='section'><div class='section-title'>Experience</div><div class='section-content'>"
    if isinstance(experience, list) and experience:
        for item in experience:
            html_content += f"""
            <div class="item">
                <span class="role">{item.get('role', 'Not Available')}</span> at <span class="company">{item.get('company', 'Not Available')}</span><br>
                {item.get('description', 'Not Available')}
            </div>
            """
    else:
        html_content += "<div class='item'>Not Available</div>"
    html_content += "</div></div>"

    # Projects Section
    projects = parsed_data.get('projects', [])
    html_content += "<div class='section'><div class='section-title'>Projects</div><div class='section-content'>"
    if isinstance(projects, list) and projects:
        for item in projects:
            html_content += f"""
            <div class="item">
                <span class="role">{item.get('name', 'Not Available')}</span><br>
                {item.get('description', 'Not Available')}
            </div>
            """
    else:
        html_content += "<div class='item'>Not Available</div>"
    html_content += "</div></div>"

    # Certifications Section
    certifications = parsed_data.get('certifications', [])
    html_content += "<div class='section'><div class='section-title'>Certifications</div><div class='section-content'><ul class='certifications-list'>"
    if isinstance(certifications, list) and certifications:
        for certification in certifications:
            html_content += f"<li class='list-item'>{certification}</li>"
    else:
        html_content += "<li class='list-item'>Not Available</li>"
    html_content += "</ul></div></div>"

    # Interests Section
    interests = parsed_data.get('interests', [])
    html_content += "<div class='section'><div class='section-title'>Interests/Hobbies</div><div class='section-content'><ul class='interests-list'>"
    if isinstance(interests, list) and interests:
        for interest in interests:
            html_content += f"<li class='list-item'>{interest}</li>"
    else:
        html_content += "<li class='list-item'>Not Available</li>"
    html_content += "</ul></div></div>"

    # Final HTML close
    html_content += """
    </body>
    </html>
    """

    # Convert HTML to PDF
    pdf_output = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_output)

    if pisa_status.err:
        raise Exception("Error generating PDF")

    pdf_output.seek(0)
    return pdf_output.read()
