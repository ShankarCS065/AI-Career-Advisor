CREATE DATABASE career_advisor;

\c career_advisor;

CREATE TABLE careers (
    id SERIAL PRIMARY KEY,
    career VARCHAR(255) NOT NULL,
    required_skills TEXT NOT NULL,
    typical_interests TEXT NOT NULL
);

INSERT INTO careers (career, required_skills, typical_interests) VALUES
('Data Scientist', 'Python, Machine Learning, SQL', 'Data Analysis, AI'),
('Software Engineer', 'Java, Kotlin, APIs', 'Problem-Solving, Development'),
('Product Manager', 'Leadership, Agile, Communication', 'Business Strategy, Innovation'),
('Cybersecurity Analyst', 'Network Security, Encryption, SIEM', 'Cybersecurity, Ethical Hacking'),
('Cloud Engineer', 'AWS, Azure, Kubernetes', 'Cloud Computing, Scalability'),
('UX Designer', 'Figma, User Research, Wireframing', 'User Experience, Design Thinking'),
('DevOps Engineer', 'Docker, CI/CD, Jenkins', 'Automation, Infrastructure'),
('AI Researcher', 'Deep Learning, TensorFlow, NLP', 'Artificial Intelligence, Research'),
('Game Developer', 'Unity, C#, Game Physics', 'Gaming, 3D Animation'),
('Full Stack Developer', 'JavaScript, React, Node.js', 'Web Development, UI/UX'),
('Blockchain Developer', 'Solidity, Smart Contracts, Ethereum', 'Decentralized Apps, Cryptography'),
('Database Administrator', 'SQL, PostgreSQL, Database Design', 'Data Management, Optimization'),
('Embedded Systems Engineer', 'C, IoT, Microcontrollers', 'Hardware Programming, Robotics'),
('IT Support Specialist', 'Troubleshooting, Windows, Linux', 'Technical Support, IT Services'),
('Digital Marketer', 'SEO, Google Ads, Social Media', 'Marketing, Branding'),
('Business Analyst', 'Data Visualization, Excel, Power BI', 'Business Insights, Decision Making'),
('Network Engineer', 'Routing, Switching, Firewalls', 'Networking, Security'),
('Robotics Engineer', 'ROS, Python, Mechanical Design', 'Automation, Robotics'),
('Mechanical Engineer', 'SolidWorks, CAD, Thermodynamics', 'Manufacturing, Mechanics'),
('Civil Engineer', 'AutoCAD, Structural Design, Surveying', 'Construction, Infrastructure'),
('Biotechnologist', 'Genetics, Bioprocess Engineering, Lab Work', 'Healthcare, Innovation'),
('Quantitative Analyst', 'Statistics, R, Financial Modeling', 'Finance, Data Analysis'),
('Economist', 'Microeconomics, Econometrics, Policy Analysis', 'Economic Research, Markets'),
('Content Writer', 'SEO, Blogging, Copywriting', 'Storytelling, Marketing'),
('Graphic Designer', 'Adobe Photoshop, Illustrator, Typography', 'Visual Arts, Creativity');

