from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_resume_pdf(jd_skills, matched, missing, file_name="generated_resume.pdf"):

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    # 🔥 CUSTOM STYLES
    name_style = ParagraphStyle(
        name="Name",
        fontSize=16,
        leading=18,
        textColor=colors.black,
        spaceAfter=6
    )

    header_style = ParagraphStyle(
        name="Header",
        fontSize=10,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        name="Section",
        fontSize=12,
        textColor=colors.darkblue,
        spaceBefore=10,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        name="Bullet",
        fontSize=10,
        leftIndent=10,
        spaceAfter=2
    )

    content = []

    # 🔥 NAME + CONTACT
    content.append(Paragraph("<b>Your Name</b>", name_style))
    content.append(Paragraph(
        "📧 your@email.com | 📞 +91-XXXXXXXXXX | GitHub | LinkedIn",
        header_style
    ))

    # 🔥 SKILLS
    content.append(Paragraph("<b>SKILLS</b>", section_style))

    content.append(Paragraph(
        f"• Core Skills: {', '.join(matched[:6] if matched else jd_skills[:6])}",
        bullet_style
    ))

    content.append(Paragraph(
        f"• Additional Skills: {', '.join(jd_skills[:8])}",
        bullet_style
    ))

    # 🔥 PROJECTS
    content.append(Paragraph("<b>PROJECTS</b>", section_style))

    for skill in jd_skills[:3]:
        content.append(Paragraph(
            f"• Developed a project using <b>{skill}</b> focusing on real-world problem solving.",
            bullet_style
        ))
        content.append(Paragraph(
            f"• Implemented efficient logic and optimized performance using {skill}.",
            bullet_style
        ))
        content.append(Paragraph(
            f"Tech Stack: {skill}, APIs, Database",
            bullet_style
        ))
        content.append(Spacer(1, 5))

    # 🔥 EXPERIENCE (AUTO GENERATED)
    content.append(Paragraph("<b>EXPERIENCE</b>", section_style))

    content.append(Paragraph(
        "• Built scalable applications and worked on real-world projects.",
        bullet_style
    ))
    content.append(Paragraph(
        "• Collaborated with teams and improved system performance.",
        bullet_style
    ))

    # 🔥 IMPROVEMENTS SECTION (IMPORTANT)
    if missing:
        content.append(Paragraph("<b>IMPROVEMENTS</b>", section_style))

        for m in missing:
            content.append(Paragraph(
                f"• Add hands-on experience in <b>{m}</b>",
                bullet_style
            ))

    # 🔥 EDUCATION
    content.append(Paragraph("<b>EDUCATION</b>", section_style))

    content.append(Paragraph(
        "Bachelor of Technology in Computer Science",
        bullet_style
    ))

    # BUILD PDF
    doc.build(content)

    return file_name