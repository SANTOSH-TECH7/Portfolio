from flask import Blueprint, render_template, send_file
from models.supabase_client import (
    get_person, get_emails, get_social_links,
    get_skill_categories, get_experience,
    get_projects, get_resume_projects,
    get_certifications, get_resume_certifications,
    get_education, get_soft_skills, get_achievements
)
from utils.resume_generator import generate_resume_pdf

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    person         = get_person()
    person_id      = person.get("id")
    emails         = get_emails(person_id) if person_id else []
    social_links   = get_social_links(person_id) if person_id else []
    skills         = get_skill_categories()
    experience     = get_experience()
    projects       = get_projects()
    certifications = get_certifications()
    education      = get_education()
    soft_skills    = get_soft_skills()
    achievements   = get_achievements()
    socials        = {s["platform"]: s["url"] for s in social_links}

    return render_template(
        "index.html",
        person=person,
        emails=emails,
        socials=socials,
        skills=skills,
        experience=experience,
        projects=projects,
        certifications=certifications,
        education=education,
        soft_skills=soft_skills,
        achievements=achievements,
    )


@public_bp.route("/resume")
def download_resume():
    person         = get_person()
    person_id      = person.get("id")
    emails         = get_emails(person_id) if person_id else []
    social_links   = get_social_links(person_id) if person_id else []
    skills         = get_skill_categories()
    experience     = get_experience()
    projects       = get_resume_projects()
    certifications = get_resume_certifications()
    education      = get_education()
    socials        = {s["platform"]: s["url"] for s in social_links}

    pdf_buffer = generate_resume_pdf(
        person, emails, socials, skills,
        experience, projects, certifications, education
    )

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="SantoshR_Resume.pdf"
    )
