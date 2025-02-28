CREATE DATABASE career_advisor;

CREATE TABLE careers (
    id SERIAL PRIMARY KEY,
    career VARCHAR(255),
    required_skills TEXT,
    typical_interests TEXT
);

INSERT INTO careers (career, required_skills, typical_interests)
VALUES 
('Data Scientist', 'Python, Machine Learning, SQL', 'Data Analysis, AI'),
('Software Engineer', 'Java, Kotlin, APIs', 'Problem-Solving, Development'),
('Product Manager', 'Leadership, Agile, Communication', 'Business Strategy, Innovation');
