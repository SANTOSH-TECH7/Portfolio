from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

BLACK      = colors.HexColor("#111111")
DARK_GRAY  = colors.HexColor("#333333")
MID_GRAY   = colors.HexColor("#666666")
LIGHT_GRAY = colors.HexColor("#999999")
WHITE      = colors.HexColor("#FFFFFF")
RULE       = colors.HexColor("#CCCCCC")
COL_W      = A4[0] - 30 * mm


def make_styles():
    return {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20,
            textColor=BLACK, alignment=TA_CENTER, leading=28),
        "role": ParagraphStyle("role", fontName="Helvetica", fontSize=10.5,
            textColor=MID_GRAY, alignment=TA_CENTER, leading=16),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8,
            textColor=MID_GRAY, alignment=TA_CENTER, leading=12),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=BLACK, spaceBefore=8, spaceAfter=3, letterSpacing=0.8),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9,
            textColor=DARK_GRAY, spaceAfter=3, leading=14),
        "muted": ParagraphStyle("muted", fontName="Helvetica", fontSize=8.5,
            textColor=MID_GRAY, spaceAfter=2, leading=13),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9,
            textColor=DARK_GRAY, spaceAfter=1, leading=13, leftIndent=12),
        "job_title": ParagraphStyle("job_title", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=BLACK, spaceAfter=0, leading=13),
        "job_date": ParagraphStyle("job_date", fontName="Helvetica", fontSize=9,
            textColor=MID_GRAY, alignment=TA_RIGHT, leading=13),
        "company": ParagraphStyle("company", fontName="Helvetica-Oblique", fontSize=9,
            textColor=MID_GRAY, spaceAfter=3, leading=13),
        "proj_title": ParagraphStyle("proj_title", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=BLACK, spaceAfter=1, leading=13),
        "proj_cat": ParagraphStyle("proj_cat", fontName="Helvetica", fontSize=8.5,
            textColor=MID_GRAY, alignment=TA_RIGHT, leading=13),
        "proj_meta": ParagraphStyle("proj_meta", fontName="Helvetica", fontSize=8.5,
            textColor=MID_GRAY, spaceAfter=2, leading=13),
        "edu_degree": ParagraphStyle("edu_degree", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=BLACK, spaceAfter=0, leading=13),
        "edu_right": ParagraphStyle("edu_right", fontName="Helvetica", fontSize=9,
            textColor=MID_GRAY, alignment=TA_RIGHT, leading=13),
        "edu_inst": ParagraphStyle("edu_inst", fontName="Helvetica", fontSize=8.5,
            textColor=MID_GRAY, spaceAfter=5, leading=13),
    }


def rule(thick=0.75, color=BLACK, after=5, before=0):
    return HRFlowable(width="100%", thickness=thick, color=color,
                      spaceAfter=after, spaceBefore=before)


def thin_rule():
    return HRFlowable(width="100%", thickness=0.3, color=RULE,
                      spaceAfter=4, spaceBefore=4)


def section_block(title, styles):
    return [Paragraph(title.upper(), styles["section"]), rule(0.75, BLACK, after=5)]


def two_col(left, right, lw=130 * mm, rw=45 * mm):
    t = Table([[left, right]], colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def generate_resume_pdf(person, emails, socials, skills,
                        experience, projects, certifications, education):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=14 * mm, bottomMargin=14 * mm)
    S = make_styles()
    story = []

    # Header
    contact_parts = [e["email"] for e in emails]
    if person.get("phone"):
        contact_parts.append(person["phone"])
    if socials.get("linkedin"):
        contact_parts.append(socials["linkedin"])
    if socials.get("github"):
        contact_parts.append(socials["github"])

    header_table = Table([
        [Paragraph(person.get("name", ""), S["name"])],
        [Paragraph(person.get("role", ""), S["role"])],
        [Paragraph("  |  ".join(contact_parts), S["contact"])],
    ], colWidths=[COL_W], rowHeights=[30, 18, 14])
    header_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(rule(1, BLACK, after=8))

    # Summary
    if person.get("summary"):
        story += section_block("Professional Summary", S)
        story.append(Paragraph(person["summary"], S["body"]))

    # Experience
    if experience:
        story += section_block("Work Experience", S)
        for exp in experience:
            start    = exp.get("start_year", "")
            end      = exp.get("end_year") or "Present"
            date_str = f"{start} – {end}" if start else ""
            block = [
                two_col(Paragraph(exp["role"], S["job_title"]),
                        Paragraph(date_str, S["job_date"])),
                Paragraph(exp["company"], S["company"]),
            ]
            for r in exp.get("responsibilities", []):
                block.append(Paragraph(f"• {r['description']}", S["bullet"]))
            if exp.get("technologies"):
                tech = ",  ".join([t["name"] for t in exp["technologies"]])
                block.append(Paragraph(f"<b>Technologies:</b>  {tech}", S["muted"]))
            block.append(Spacer(1, 4))
            story.append(KeepTogether(block))

    # Skills
    if skills:
        story += section_block("Technical Skills", S)
        for cat in skills:
            if cat.get("skills"):
                names = ",  ".join([s["name"] for s in cat["skills"]])
                story.append(Paragraph(f"<b>{cat['name']}:</b>  {names}", S["body"]))

    # Projects
    if projects:
        story += section_block("Projects", S)
        for p in projects:
            block = [two_col(Paragraph(p["title"], S["proj_title"]),
                             Paragraph(p.get("category", ""), S["proj_cat"]))]
            if p.get("metrics"):
                m_str = "  |  ".join([f"{m['metric_name']}: {m['value']}" for m in p["metrics"]])
                block.append(Paragraph(m_str, S["proj_meta"]))
            if p.get("description"):
                block.append(Paragraph(p["description"], S["body"]))
            if p.get("tools"):
                tools = ",  ".join([t["name"] for t in p["tools"]])
                block.append(Paragraph(f"<b>Tools:</b>  {tools}", S["muted"]))
            if p.get("github_url"):
                block.append(Paragraph(f"<b>GitHub:</b>  {p['github_url']}", S["muted"]))
            block.append(thin_rule())
            story.append(KeepTogether(block))

    # Education
    edu_list = sorted(education, key=lambda x: x.get("sort_order", 99))
    if edu_list:
        edu_block = section_block("Education", S)
        for edu in edu_list:
            right_parts = []
            if edu.get("year"):
                right_parts.append(edu["year"])
            if edu.get("percentage"):
                right_parts.append(edu["percentage"])
            right_str = "  |  ".join(right_parts)
            inst_line = edu["institution"]
            if edu.get("place"):
                inst_line += f"  —  {edu['place']}"
            if edu.get("status"):
                inst_line += f"  ({edu['status']})"
            edu_block += [
                two_col(Paragraph(edu["degree"], S["edu_degree"]),
                        Paragraph(right_str, S["edu_right"])),
                Paragraph(inst_line, S["edu_inst"]),
            ]
        story.append(KeepTogether(edu_block))

    # Certifications
    if certifications:
        cert_block = section_block("Certifications", S)
        for c in certifications:
            dur      = f"  ({c['duration']})" if c.get("duration") else ""
            platform = f"  —  {c['platform']}" if c.get("platform") else ""
            cert_block.append(Paragraph(f"• <b>{c['name']}</b>{dur}{platform}", S["bullet"]))
        story.append(KeepTogether(cert_block))

    def white_bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(WHITE)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.restoreState()

    doc.build(story, onFirstPage=white_bg, onLaterPages=white_bg)
    buffer.seek(0)
    return buffer
