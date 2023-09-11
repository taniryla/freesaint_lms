CREATE DATABASE freesaint_lms;

CREATE TABLE lms_logins (
	login_id SERIAL PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

CREATE TABLE app_users (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	googleId TEXT NOT NULL UNIQUE,
	GWTToken TEXT NOT NULL UNIQUE,
	profile_active BOOLEAN,
	calculated_cal_goal INT,
	starting_weight INT,
	target_weight INT,
	avatar_photo JSON,
	age INT,
	height INT
);

CREATE TABLE lms_courses (
    course_id SERIAL PRIMARY KEY,
    course_name TEXT NOT NULL,
    course_type TEXT NOT NULL,
    course_stu_id TEXT NOT NULL UNIQUE,
    course_description TEXT NOT NULL,
    completed BOOLEAN NOT NULL,
    quizzes TEXT NOT NULL
);

CREATE TABLE lms_permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_name TEXT NOT NULL,
    permission_module TEXT NOT NULL UNIQUE
);

CREATE TABLE lms_quizzes (
    quiz_id SERIAL PRIMARY KEY,
    quiz_name TEXT NOT NULL UNIQUE,
    quiz_type TEXT NOT NULL
);

CREATE TABLE lms_chatgpt_sources (
    id SERIAL PRIMARY KEY,
    podcast_transcripts TEXT NOT NULL,
    youtube_transcripts TEXT NOT NULL,
    health_blogs TEXT NOT NULL,
    health_wikis TEXT NOT NULL,
    health_book_libraries TEXT NOT NULL,
    health_web_scrapes TEXT NOT NULL,
    recipes TEXT NOT NULL
);

CREATE TABLE lms_topics (
    id SERIAL PRIMARY KEY,
    gut_health TEXT NOT NULL,
    hormones TEXT NOT NULL,
    weight_loss TEXT NOT NULL,
    mommy_makeover TEXT NOT NULL,
    vegan TEXT NOT NULL,
    keto TEXT NOT NULL,
    vegetarian TEXT NOT NULL,
    pescatarian TEXT NOT NULL,
    intermittent_fasting TEXT NOT NULL,
    nutrition TEXT NOT NULL,
    cardio TEXT NOT NULL,
    habits_motivation TEXT NOT NULL,
    neuroscience_food TEXT NOT NULL,
    LOA_manifesting TEXT NOT NULL,
    selfcare_sleep_stress TEXT NOT NULL,
    vagus_nerve TEXT NOT NULL,
    meditation TEXT NOT NULL,
    yoga TEXT NOT NULL,
    pilates TEXT NOT NULL,
    nature TEXT NOT NULL,
    weight_lifting TEXT NOT NULL,
    hiits TEXT NOT NULL
);

-- 1-to-1 relationship 

ALTER TABLE lms_logins
ADD CONSTRAINT fk_lms_logins_app_users
FOREIGN KEY (login_id)
REFERENCES app_users;


-- 1-to-many relationships

ALTER TABLE lms_permissions
ADD CONSTRAINT fk_lms_permissions_lms_logins
FOREIGN KEY (permission_id)
REFERENCES lms_logins;

ALTER TABLE lms_quizzes
ADD CONSTRAINT fk_lms_quizzes_lms_courses
FOREIGN KEY (quiz_id)
REFERENCES lms_courses;

ALTER TABLE lms_chatgpt_sources
ADD CONSTRAINT fk_lms_chatgpt_sources_lms_courses
FOREIGN KEY (id)
REFERENCES lms_courses;

-- many-to-many relationships

ALTER TABLE lms_courses
ADD CONSTRAINT fk_lms_courses_lms_permissions
FOREIGN KEY (course_id)
REFERENCES lms_permissions;

ALTER TABLE lms_topics
ADD CONSTRAINT fk_lms_topics_lms_chatgpt_sources
FOREIGN KEY (id)
REFERENCES lms_chatgpt_sources;

-- add in values

INSERT INTO app_users (name, email, profile_active, calculated_cal_goal, starting_weight, target_weight, age, height)
VALUES ('Chako Arai', 'chakoarai7@gmail.com', 'True', 1850, 158, 125, 45, 176);

INSERT INTO lms_logins (login_id, username, password)
VALUES (7145, 'chakoarai', 'password123');

INSERT INTO lms_courses (course_name, course_type, course_description, completed)
VALUES ('Leaky Gut', 'online', 'lose weight by reducing your leaky gut', False);
