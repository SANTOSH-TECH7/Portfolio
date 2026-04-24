-- ============================================================
-- SANTOSH R — PORTFOLIO APP SUPABASE SCHEMA
-- Run this ENTIRE file in Supabase SQL Editor → New Query → Run
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── PERSONS ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS persons (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name              TEXT NOT NULL,
    phone             TEXT,
    role              TEXT,
    summary           TEXT,
    age               INT,
    profile_image_url TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ── EMAILS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS emails (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES persons(id) ON DELETE CASCADE,
    email     TEXT NOT NULL
);

-- ── SOCIAL LINKS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS social_links (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES persons(id) ON DELETE CASCADE,
    platform  TEXT NOT NULL,
    url       TEXT NOT NULL
);

-- ── SKILL CATEGORIES ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skill_categories (
    id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

-- ── SKILLS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skills (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID REFERENCES skill_categories(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    percentage  INT DEFAULT 80
);

-- ── WORK EXPERIENCE ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS work_experience (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id  UUID REFERENCES persons(id) ON DELETE CASCADE,
    role       TEXT NOT NULL,
    company    TEXT NOT NULL,
    duration   TEXT,
    start_year TEXT,
    end_year   TEXT
);

-- ── EXPERIENCE RESPONSIBILITIES ──────────────────────────────
CREATE TABLE IF NOT EXISTS experience_responsibilities (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experience_id UUID REFERENCES work_experience(id) ON DELETE CASCADE,
    description   TEXT NOT NULL
);

-- ── EXPERIENCE TECHNOLOGIES ──────────────────────────────────
CREATE TABLE IF NOT EXISTS experience_technologies (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experience_id UUID REFERENCES work_experience(id) ON DELETE CASCADE,
    name          TEXT NOT NULL
);

-- ── PROJECTS ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id         UUID REFERENCES persons(id) ON DELETE CASCADE,
    title             TEXT NOT NULL,
    description       TEXT,
    category          TEXT,
    github_url        TEXT,
    demo_url          TEXT,
    image_url         TEXT,
    include_in_resume BOOLEAN DEFAULT TRUE
);

-- ── PROJECT METRICS ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_metrics (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id  UUID REFERENCES projects(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    value       TEXT NOT NULL
);

-- ── PROJECT TOOLS ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_tools (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name       TEXT NOT NULL
);

-- ── PROJECT ALGORITHMS ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_algorithms (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name       TEXT NOT NULL
);

-- ── ACHIEVEMENTS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS achievements (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id     UUID REFERENCES persons(id) ON DELETE CASCADE,
    title         TEXT NOT NULL,
    subtitle      TEXT,
    description   TEXT,
    icon          TEXT DEFAULT 'fas fa-trophy',
    display_order INT  DEFAULT 99
);

-- ── CERTIFICATIONS ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certifications (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id            UUID REFERENCES persons(id) ON DELETE CASCADE,
    name                 TEXT NOT NULL,
    platform             TEXT,
    duration             TEXT,
    start_date           DATE,
    include_in_resume    BOOLEAN DEFAULT TRUE
);

-- ── EDUCATION ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS education (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id   UUID REFERENCES persons(id) ON DELETE CASCADE,
    degree      TEXT NOT NULL,
    institution TEXT NOT NULL,
    place       TEXT,
    year        TEXT,
    percentage  TEXT,
    status      TEXT,
    sort_order  INT DEFAULT 99
);

-- ── SOFT SKILLS ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS soft_skills (
    id        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES persons(id) ON DELETE CASCADE,
    name      TEXT NOT NULL
);

-- ── RESUME FILES ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resume_files (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id   UUID REFERENCES persons(id) ON DELETE CASCADE,
    file_url    TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SEED DATA — Santosh R
-- ============================================================

-- Step 1: Insert person
INSERT INTO persons (name, phone, role, age, summary, profile_image_url)
VALUES (
    'Santosh R',
    NULL,
    'AI & Data Science Engineer',
    NULL,
    'A passionate AI and Data Science student at V.S.B Engineering College, Karur, specializing in machine learning, deep learning, and full-stack development. Department representative with hands-on experience building intelligent applications using Python, TensorFlow, OpenCV, Flask, and Selenium. Driven by solving real-world problems through data-driven solutions.',
    'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg'
) RETURNING id;

-- !! COPY THE UUID FROM ABOVE OUTPUT AND REPLACE <PERSON_UUID> IN ALL INSERTS BELOW !!

-- Step 2: Email
-- INSERT INTO emails (person_id, email) VALUES ('<PERSON_UUID>', 'santoshravi.san.2004@gmail.com');

-- Step 3: Social links
-- INSERT INTO social_links (person_id, platform, url) VALUES ('<PERSON_UUID>', 'github',     'https://github.com/SANTOSH-TECH7');
-- INSERT INTO social_links (person_id, platform, url) VALUES ('<PERSON_UUID>', 'linkedin',   'https://www.linkedin.com/in/santosh-ravi1804');
-- INSERT INTO social_links (person_id, platform, url) VALUES ('<PERSON_UUID>', 'leetcode',   'https://leetcode.com/u/Santosh_R/');
-- INSERT INTO social_links (person_id, platform, url) VALUES ('<PERSON_UUID>', 'hackerrank', 'https://www.hackerrank.com/profile/santosh88386r');

-- Step 4: Skill categories + skills
-- Run each INSERT INTO skill_categories ... RETURNING id;
-- Copy each returned UUID and use it in the skills inserts below.

-- INSERT INTO skill_categories (name) VALUES ('Programming Languages') RETURNING id;
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Python',     95);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'JavaScript', 85);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'HTML & CSS', 90);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Java',       75);

-- INSERT INTO skill_categories (name) VALUES ('AI & Machine Learning') RETURNING id;
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Machine Learning', 90);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'TensorFlow',       85);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'OpenCV',           85);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Scikit-Learn',     88);

-- INSERT INTO skill_categories (name) VALUES ('Frameworks & Tools') RETURNING id;
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Flask',     80);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Django',    75);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Selenium',  88);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Tkinter',   80);

-- INSERT INTO skill_categories (name) VALUES ('Databases & Cloud') RETURNING id;
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'SQL',    82);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'Docker', 70);
-- INSERT INTO skills (category_id, name, percentage) VALUES ('<CAT_UUID>', 'AWS',    68);

-- Step 5: Projects (replace <PERSON_UUID>)
-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'CodeFixPro',
--  'An AI-driven tool for automatically detecting and suggesting fixes for coding errors. Built using Python and ML models to help developers quickly debug code and learn better practices.',
--  'AI / NLP',
--  'https://github.com/SANTOSH-TECH7/CodeFixPro',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWbqm_Px5A3wFEABLUwVYQMhOQpY04juKxZQ&s')
-- RETURNING id;
-- -- Copy project id → <P1_UUID>
-- INSERT INTO project_tools (project_id, name) VALUES ('<P1_UUID>','Python'),('<P1_UUID>','Machine Learning'),('<P1_UUID>','NLP'),('<P1_UUID>','Code Analysis');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'LinkedIn_Bot',
--  'A Python automation bot for LinkedIn using Selenium, capable of connecting with professionals, sending personalized messages, and enhancing professional networking at scale.',
--  'Automation',
--  'https://github.com/SANTOSH-TECH7/LinkedIn_Bot',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0YJYgYDXqgC1tLVuC2sxcLtJ4B8RAlq48cw&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P2_UUID>','Python'),('<P2_UUID>','Selenium'),('<P2_UUID>','Web Automation');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'EPILEPSY-MODEL-TRAINING',
--  'Deep learning project focused on training a model to detect epileptic seizures using EEG data. Involves model optimization, evaluation metrics, and real-time application potential.',
--  'Deep Learning / Medical AI',
--  'https://github.com/SANTOSH-TECH7/EPILEPSY-MODEL-TRAINING',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSctEjU0e8sap3V4HSAZEqUWAKJv8KsKYMadQ&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P3_UUID>','Deep Learning'),('<P3_UUID>','TensorFlow'),('<P3_UUID>','EEG Analysis');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'Smart-Attendance-System',
--  'A face recognition-based attendance system using OpenCV and ML that marks and stores attendance efficiently, eliminating manual entry and improving accuracy.',
--  'Computer Vision',
--  'https://github.com/SANTOSH-TECH7/Smart-Attendance-System-Using-Face-Recognition',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYsMgskvvvZMr652FOav3kNJ1mch8kWtmnuA&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P4_UUID>','OpenCV'),('<P4_UUID>','Python'),('<P4_UUID>','Face Recognition');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'Heart_Disease_Prediction',
--  'A machine learning model trained using logistic regression to predict the likelihood of heart disease using health indicators from medical datasets.',
--  'ML / Healthcare',
--  'https://github.com/SANTOSH-TECH7/Heart_Disease_Prediction-using-LogisticRegression',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWeuNWMaZIyEI82lzg003P5Qw5MOVPmO14Ew&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P5_UUID>','Logistic Regression'),('<P5_UUID>','Scikit-Learn'),('<P5_UUID>','Data Analysis');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'Task-Remainder-Automation',
--  'A Python automation script that reminds users of tasks at specified intervals using Tkinter and voice alerts — enhancing daily productivity.',
--  'Automation',
--  'https://github.com/SANTOSH-TECH7/Task-Remainder-Automation',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSmwx1n8p2ta1F_8eYt26NTgeNuWuISNqa3w&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P6_UUID>','Python'),('<P6_UUID>','Tkinter'),('<P6_UUID>','Automation');

-- INSERT INTO projects (person_id, title, description, category, github_url, image_url) VALUES
-- ('<PERSON_UUID>', 'Water_app',
--  'A complete water usage chatbot solution that calculates water footprints (blue, green, grey) based on user inputs. Built with Python backend, front-end integration, and fuzzy matching for optimal UX.',
--  'Web / AI',
--  'https://github.com/SANTOSH-TECH7/Water_app',
--  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuTxTo4kuaUSxosEnPYIKQSDeylxFFduiTWg&s')
-- RETURNING id;
-- INSERT INTO project_tools (project_id, name) VALUES ('<P7_UUID>','Python'),('<P7_UUID>','ChatBot'),('<P7_UUID>','Fuzzy Matching'),('<P7_UUID>','Web Integration');

-- Step 6: Achievements
-- INSERT INTO achievements (person_id, title, subtitle, description, icon, display_order) VALUES
-- ('<PERSON_UUID>', 'MSME National Competition', 'Shortlisted in Top 25 Teams',
--  'Recognized for innovative solutions in Sustainable Management and Development in Water FootPrint.',
--  'fas fa-trophy', 1),
-- ('<PERSON_UUID>', 'Kongu Engineering College', '1st & 2nd Prize',
--  'Won prizes for AI-Powered Seizure Detection and Sustainable Fashion AI Solutions projects.',
--  'fas fa-medal', 2),
-- ('<PERSON_UUID>', 'Hands-On-Training', 'LABView Tool & Its Applications',
--  'Completed comprehensive training at PSG Engineering College.',
--  'fas fa-certificate', 3);

-- Step 7: Certifications
-- INSERT INTO certifications (person_id, name, platform, duration, start_date) VALUES
-- ('<PERSON_UUID>', 'Internship on AI', 'Novi Tech R&D Private Limited', NULL, '2023-01-01'),
-- ('<PERSON_UUID>', 'Gemini AI Jarvis Workshop', 'LetsUpgrade', NULL, '2024-01-01');

-- Step 8: Education
-- INSERT INTO education (person_id, degree, institution, place, status, sort_order) VALUES
-- ('<PERSON_UUID>', 'B.Tech in Artificial Intelligence & Data Science', 'V.S.B Engineering College', 'Karur, Tamil Nadu', 'Currently Pursuing', 1);

-- Step 9: Soft Skills
-- INSERT INTO soft_skills (person_id, name) VALUES
-- ('<PERSON_UUID>', 'Problem Solving'),
-- ('<PERSON_UUID>', 'Team Collaboration'),
-- ('<PERSON_UUID>', 'Analytical Thinking'),
-- ('<PERSON_UUID>', 'Communication'),
-- ('<PERSON_UUID>', 'Adaptability'),
-- ('<PERSON_UUID>', 'Leadership');

-- ============================================================
-- SUPABASE AUTH USER
-- Go to: Supabase Dashboard → Authentication → Users → Add User
-- Email   : santoshravi.san.2004@gmail.com
-- Password: (set your own strong password)
-- ============================================================
