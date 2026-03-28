CREATE TABLE IF NOT EXISTS abstract (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    submitted_by INT NOT NULL,
    title TEXT NOT NULL,
    abstract_text TEXT NOT NULL,
    keywords TEXT,
    track VARCHAR(200),
    presentation_type ENUM('oral','poster','either') NOT NULL DEFAULT 'either',
    status ENUM('submitted','under_review','accepted','rejected','revision_required') NOT NULL DEFAULT 'submitted',
    word_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (submitted_by) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS abstract_author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    abstract_id INT NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(200),
    affiliation VARCHAR(300),
    country VARCHAR(100),
    is_presenting BOOLEAN DEFAULT FALSE,
    author_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (abstract_id) REFERENCES abstract(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS abstract_reviewer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    abstract_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    UNIQUE KEY unique_abstract_reviewer (abstract_id, reviewer_id),
    FOREIGN KEY (abstract_id) REFERENCES abstract(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES user(id),
    FOREIGN KEY (assigned_by) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS abstract_review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL UNIQUE,
    relevance_score INT NOT NULL,
    methodology_score INT NOT NULL,
    originality_score INT NOT NULL,
    overall_score INT NOT NULL,
    recommendation ENUM('accept','reject','revision_required') NOT NULL,
    comments TEXT NOT NULL,
    confidential_comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES abstract_reviewer(id) ON DELETE CASCADE
);
