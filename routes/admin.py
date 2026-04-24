from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from config import ADMIN_EMAIL
from models.supabase_client import (
    get_person, update_person,
    get_emails, add_email, delete_email,
    get_social_links, upsert_social_link,
    get_skill_categories, add_skill, update_skill, delete_skill,
    add_skill_category, delete_skill_category,
    get_experience, add_experience, update_experience, delete_experience,
    add_responsibility, delete_responsibility,
    add_exp_technology, delete_exp_technology,
    get_projects, get_project, add_project, update_project, delete_project,
    toggle_resume_project,
    add_project_tool, add_project_metric, add_project_algorithm,
    get_achievements, add_achievement, update_achievement, delete_achievement,
    get_certifications, add_certification, update_certification, delete_certification,
    toggle_resume_certification,
    get_education, add_education, update_education, delete_education,
    get_soft_skills, add_soft_skill, delete_soft_skill,
)
from models.supabase_client import supabase

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


# ── AUTH ─────────────────────────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                session["admin_logged_in"] = True
                session["admin_email"]     = email
                flash("Welcome back!", "success")
                return redirect(url_for("admin.dashboard"))
        except Exception:
            flash("Invalid credentials. Try again.", "danger")
    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("public.index"))


# ── DASHBOARD ────────────────────────────────────────────────
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    person         = get_person()
    projects       = get_projects()
    skills         = get_skill_categories()
    certifications = get_certifications()
    education      = get_education()
    soft_skills    = get_soft_skills()
    experience     = get_experience()
    achievements   = get_achievements()
    return render_template(
        "dashboard.html",
        person=person,
        projects=projects,
        skills=skills,
        certifications=certifications,
        education=education,
        soft_skills=soft_skills,
        experience=experience,
        achievements=achievements,
    )


# ── PROFILE ──────────────────────────────────────────────────
@admin_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    person = get_person()
    if request.method == "POST":
        data = {
            "name":              request.form.get("name"),
            "phone":             request.form.get("phone"),
            "role":              request.form.get("role"),
            "summary":           request.form.get("summary"),
            "age":               request.form.get("age") or None,
            "profile_image_url": request.form.get("profile_image_url") or None,
        }
        update_person(person["id"], data)
        for platform in ["github", "linkedin", "leetcode", "hackerrank"]:
            url = request.form.get(platform)
            if url:
                upsert_social_link(person["id"], platform, url)
        flash("Profile updated.", "success")
        return redirect(url_for("admin.dashboard"))
    socials = {s["platform"]: s["url"] for s in get_social_links(person["id"])}
    return render_template("edit_profile.html", person=person, socials=socials)


# ── PROJECTS ─────────────────────────────────────────────────
@admin_bp.route("/add-project", methods=["GET", "POST"])
@login_required
def add_project_route():
    if request.method == "POST":
        person = get_person()
        data = {
            "person_id":         person["id"],
            "title":             request.form.get("title"),
            "description":       request.form.get("description"),
            "category":          request.form.get("category"),
            "github_url":        request.form.get("github_url"),
            "demo_url":          request.form.get("demo_url"),
            "image_url":         request.form.get("image_url") or None,
        }
        res        = add_project(data)
        project_id = res.data[0]["id"]
        for t in [x.strip() for x in request.form.get("tools", "").split(",") if x.strip()]:
            add_project_tool(project_id, t)
        metric_name  = request.form.get("metric_name")
        metric_value = request.form.get("metric_value")
        if metric_name and metric_value:
            add_project_metric(project_id, metric_name, metric_value)
        flash("Project added.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("add_project.html")


@admin_bp.route("/edit-project/<project_id>", methods=["GET", "POST"])
@login_required
def edit_project_route(project_id):
    project = get_project(project_id)
    if request.method == "POST":
        update_project(project_id, {
            "title":       request.form.get("title"),
            "description": request.form.get("description"),
            "category":    request.form.get("category"),
            "github_url":  request.form.get("github_url"),
            "demo_url":    request.form.get("demo_url"),
            "image_url":   request.form.get("image_url") or None,
        })
        flash("Project updated.", "success")
        return redirect(url_for("admin.edit_project_route", project_id=project_id))
    return render_template("edit_project.html", project=project)


@admin_bp.route("/add-project-tool/<project_id>", methods=["POST"])
@login_required
def add_project_tool_route(project_id):
    add_project_tool(project_id, request.form.get("name"))
    flash("Tool added.", "success")
    return redirect(url_for("admin.edit_project_route", project_id=project_id))


@admin_bp.route("/delete-project-tool/<project_id>/<tool_id>")
@login_required
def delete_project_tool_route(project_id, tool_id):
    from models.supabase_client import supabase as sb
    sb.table("project_tools").delete().eq("id", tool_id).execute()
    flash("Tool deleted.", "success")
    return redirect(url_for("admin.edit_project_route", project_id=project_id))


@admin_bp.route("/add-project-metric/<project_id>", methods=["POST"])
@login_required
def add_project_metric_route(project_id):
    add_project_metric(project_id, request.form.get("metric_name"), request.form.get("metric_value"))
    flash("Metric added.", "success")
    return redirect(url_for("admin.edit_project_route", project_id=project_id))


@admin_bp.route("/delete-project-metric/<project_id>/<metric_id>")
@login_required
def delete_project_metric_route(project_id, metric_id):
    from models.supabase_client import supabase as sb
    sb.table("project_metrics").delete().eq("id", metric_id).execute()
    flash("Metric deleted.", "success")
    return redirect(url_for("admin.edit_project_route", project_id=project_id))


@admin_bp.route("/delete-project/<project_id>")
@login_required
def delete_project_route(project_id):
    delete_project(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/toggle-resume-project/<project_id>")
@login_required
def toggle_resume_project_route(project_id):
    project = get_project(project_id)
    current = project.get("include_in_resume", True)
    toggle_resume_project(project_id, not current)
    status = "included in" if not current else "excluded from"
    flash(f"'{project['title']}' {status} resume.", "success")
    return redirect(url_for("admin.dashboard"))


# ── SKILLS ───────────────────────────────────────────────────
@admin_bp.route("/add-skill", methods=["GET", "POST"])
@login_required
def add_skill_route():
    categories = get_skill_categories()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_category":
            add_skill_category(request.form.get("category_name"))
            flash("Category added.", "success")
        else:
            add_skill(
                request.form.get("category_id"),
                request.form.get("name"),
                int(request.form.get("percentage", 80))
            )
            flash("Skill added.", "success")
        return redirect(url_for("admin.add_skill_route"))
    return render_template("add_skill.html", categories=categories)


@admin_bp.route("/delete-skill/<skill_id>")
@login_required
def delete_skill_route(skill_id):
    delete_skill(skill_id)
    flash("Skill deleted.", "success")
    return redirect(url_for("admin.add_skill_route"))


@admin_bp.route("/edit-skill/<skill_id>", methods=["POST"])
@login_required
def edit_skill_route(skill_id):
    update_skill(skill_id, request.form.get("name"), int(request.form.get("percentage", 80)))
    flash("Skill updated.", "success")
    return redirect(url_for("admin.add_skill_route"))


@admin_bp.route("/delete-skill-category/<cat_id>")
@login_required
def delete_skill_category_route(cat_id):
    delete_skill_category(cat_id)
    flash("Category and all its skills deleted.", "success")
    return redirect(url_for("admin.add_skill_route"))


# ── ACHIEVEMENTS ─────────────────────────────────────────────
@admin_bp.route("/add-achievement", methods=["GET", "POST"])
@login_required
def add_achievement_route():
    achievements = get_achievements()
    if request.method == "POST":
        person = get_person()
        add_achievement({
            "person_id":     person["id"],
            "title":         request.form.get("title"),
            "subtitle":      request.form.get("subtitle") or None,
            "description":   request.form.get("description") or None,
            "icon":          request.form.get("icon") or "fas fa-trophy",
            "display_order": int(request.form.get("display_order", 99)),
        })
        flash("Achievement added.", "success")
        return redirect(url_for("admin.add_achievement_route"))
    return render_template("add_achievement.html", achievements=achievements)


@admin_bp.route("/edit-achievement/<ach_id>", methods=["POST"])
@login_required
def edit_achievement_route(ach_id):
    update_achievement(ach_id, {
        "title":         request.form.get("title"),
        "subtitle":      request.form.get("subtitle") or None,
        "description":   request.form.get("description") or None,
        "icon":          request.form.get("icon") or "fas fa-trophy",
        "display_order": int(request.form.get("display_order", 99)),
    })
    flash("Achievement updated.", "success")
    return redirect(url_for("admin.add_achievement_route"))


@admin_bp.route("/delete-achievement/<ach_id>")
@login_required
def delete_achievement_route(ach_id):
    delete_achievement(ach_id)
    flash("Achievement deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── CERTIFICATIONS ───────────────────────────────────────────
@admin_bp.route("/add-certification", methods=["GET", "POST"])
@login_required
def add_certification_route():
    certifications = get_certifications()
    if request.method == "POST":
        person = get_person()
        add_certification({
            "person_id":  person["id"],
            "name":       request.form.get("name"),
            "platform":   request.form.get("platform"),
            "duration":   request.form.get("duration"),
            "start_date": request.form.get("start_date") or None,
        })
        flash("Certification added.", "success")
        return redirect(url_for("admin.add_certification_route"))
    return render_template("add_certification.html", certifications=certifications)


@admin_bp.route("/edit-certification/<cert_id>", methods=["POST"])
@login_required
def edit_certification_route(cert_id):
    update_certification(cert_id, {
        "name":       request.form.get("name"),
        "platform":   request.form.get("platform"),
        "duration":   request.form.get("duration"),
        "start_date": request.form.get("start_date") or None,
    })
    flash("Certification updated.", "success")
    return redirect(url_for("admin.add_certification_route"))


@admin_bp.route("/delete-certification/<cert_id>")
@login_required
def delete_certification_route(cert_id):
    delete_certification(cert_id)
    flash("Certification deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/toggle-resume-certification/<cert_id>")
@login_required
def toggle_resume_certification_route(cert_id):
    certs = get_certifications()
    cert  = next((c for c in certs if c["id"] == cert_id), None)
    if cert:
        current = cert.get("include_in_resume", True)
        toggle_resume_certification(cert_id, not current)
        status = "included in" if not current else "excluded from"
        flash(f"'{cert['name']}' {status} resume.", "success")
    return redirect(url_for("admin.dashboard"))


# ── EDUCATION ────────────────────────────────────────────────
@admin_bp.route("/add-education", methods=["GET", "POST"])
@login_required
def add_education_route():
    education = get_education()
    if request.method == "POST":
        person = get_person()
        add_education({
            "person_id":   person["id"],
            "degree":      request.form.get("degree"),
            "institution": request.form.get("institution"),
            "place":       request.form.get("place"),
            "year":        request.form.get("year") or None,
            "percentage":  request.form.get("percentage") or None,
            "status":      request.form.get("status") or None,
            "sort_order":  int(request.form.get("sort_order", 99)),
        })
        flash("Education added.", "success")
        return redirect(url_for("admin.add_education_route"))
    return render_template("add_education.html", education=education)


@admin_bp.route("/edit-education/<edu_id>", methods=["POST"])
@login_required
def edit_education_route(edu_id):
    update_education(edu_id, {
        "degree":      request.form.get("degree"),
        "institution": request.form.get("institution"),
        "place":       request.form.get("place"),
        "year":        request.form.get("year") or None,
        "percentage":  request.form.get("percentage") or None,
        "status":      request.form.get("status") or None,
        "sort_order":  int(request.form.get("sort_order", 99)),
    })
    flash("Education updated.", "success")
    return redirect(url_for("admin.add_education_route"))


@admin_bp.route("/delete-education/<edu_id>")
@login_required
def delete_education_route(edu_id):
    delete_education(edu_id)
    flash("Education deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── SOFT SKILLS ──────────────────────────────────────────────
@admin_bp.route("/add-soft-skill", methods=["POST"])
@login_required
def add_soft_skill_route():
    person = get_person()
    add_soft_skill(person["id"], request.form.get("name"))
    flash("Soft skill added.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete-soft-skill/<skill_id>")
@login_required
def delete_soft_skill_route(skill_id):
    delete_soft_skill(skill_id)
    flash("Soft skill deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── EXPERIENCE ───────────────────────────────────────────────
@admin_bp.route("/manage-experience")
@login_required
def manage_experience():
    experience = get_experience()
    return render_template("manage_experience.html", experience=experience)


@admin_bp.route("/add-experience", methods=["POST"])
@login_required
def add_experience_route():
    person = get_person()
    add_experience({
        "person_id":  person["id"],
        "role":       request.form.get("role"),
        "company":    request.form.get("company"),
        "start_year": request.form.get("start_year") or None,
        "end_year":   request.form.get("end_year") or None,
        "duration":   request.form.get("duration") or None,
    })
    flash("Job added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/edit-experience/<exp_id>", methods=["POST"])
@login_required
def edit_experience_route(exp_id):
    update_experience(exp_id, {
        "role":       request.form.get("role"),
        "company":    request.form.get("company"),
        "start_year": request.form.get("start_year") or None,
        "end_year":   request.form.get("end_year") or None,
        "duration":   request.form.get("duration") or None,
    })
    flash("Experience updated.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-experience/<exp_id>")
@login_required
def delete_experience_route(exp_id):
    delete_experience(exp_id)
    flash("Job deleted.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/add-responsibility/<exp_id>", methods=["POST"])
@login_required
def add_responsibility_route(exp_id):
    add_responsibility(exp_id, request.form.get("description"))
    flash("Responsibility added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-responsibility/<resp_id>")
@login_required
def delete_responsibility_route(resp_id):
    delete_responsibility(resp_id)
    flash("Responsibility deleted.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/add-exp-technology/<exp_id>", methods=["POST"])
@login_required
def add_exp_technology_route(exp_id):
    add_exp_technology(exp_id, request.form.get("name"))
    flash("Technology added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-exp-technology/<tech_id>")
@login_required
def delete_exp_technology_route(tech_id):
    delete_exp_technology(tech_id)
    flash("Technology deleted.", "success")
    return redirect(url_for("admin.manage_experience"))
