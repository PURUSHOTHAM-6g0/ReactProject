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
                margin-bottom: 20px;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 2px;
            }}
            hr {{
                border: 0;
                border-top: 1px solid #ccc;
                margin: 5px 0 10px 0;
            }}
            .section-content {{
                margin-left: 20px;
                font-size: 14px;
            }}
            .item {{
                margin-bottom: 6px;
            }}
            .degree, .role {{
                font-weight: bold;
            }}
            .institution, .company {{
                font-style: italic;
            }}
            .skills-list {{
                padding: 0;
                margin: 0;
            }}
            .skills-list li {{
                display: inline-block;
                margin-right: 10px;
                margin-bottom: 5px;
            }}
            .certifications-list, .interests-list {{
                margin-left: 20px;
                padding-left: 0;
            }}
            .certifications-list li,
            .interests-list li {{
                margin-bottom: 5px;
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
    html_content += "<div class='section'><div class='section-title'>Education</div><hr><div class='section-content'>"
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
    html_content += "<div class='section'><div class='section-title'>Skills</div><hr><div class='section-content'>"
    if isinstance(skills, list) and skills:
        skills_str = ', '.join(skills)
        html_content += f"<p>{skills_str}</p>"
    else:
        html_content += "<p>Not Available</p>"
    html_content += "</div></div>"

    # Experience Section
    experience = parsed_data.get('experience', [])
    html_content += "<div class='section'><div class='section-title'>Experience</div><hr><div class='section-content'>"
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
    html_content += "<div class='section'><div class='section-title'>Projects</div><hr><div class='section-content'>"
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
    html_content += "<div class='section'><div class='section-title'>Certifications</div><hr><div class='section-content'><ul class='certifications-list'>"
    if isinstance(certifications, list) and certifications:
        for certification in certifications:
            html_content += f"<li class='list-item'>{certification}</li>"
    else:
        html_content += "<li class='list-item'>Not Available</li>"
    html_content += "</ul></div></div>"

    # Interests Section
    interests = parsed_data.get('interests', [])
    html_content += "<div class='section'><div class='section-title'>Interests/Hobbies</div><hr><div class='section-content'><ul class='interests-list'>"
    if isinstance(interests, list) and interests:
        for interest in interests:
            html_content += f"<li class='list-item'>{interest}</li>"
    else:
        html_content += "<li class='list-item'>Not Available</li>"
    html_content += "</ul></div></div>"

    html_content += """
    </body>
    </html>
    """

    pdf_output = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_output)

    if pisa_status.err:
        raise Exception("Error generating PDF")

    pdf_output.seek(0)
    return pdf_output.read()
