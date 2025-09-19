drop database icf_db_v1;
create database icf_db_v1;
use icf_db_v1;

CREATE TABLE icf_category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) UNIQUE NOT NULL,     -- e.g. "b280"
    description VARCHAR(255) NOT NULL    -- e.g. "Sensation of pain"
);

CREATE TABLE core_set (
    core_set_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,           -- e.g. "Low Back Pain Brief"
    has_comprehensive BOOLEAN DEFAULT 0   -- flag to say if comp set exists
);

CREATE TABLE core_set_category (
    core_set_id INT,
    category_id INT,
    PRIMARY KEY (core_set_id, category_id),
    FOREIGN KEY (core_set_id) REFERENCES core_set(core_set_id),
    FOREIGN KEY (category_id) REFERENCES icf_category(category_id)
);

CREATE TABLE comp_core_set_category (
    core_set_id INT,
    category_id INT,
    PRIMARY KEY (core_set_id, category_id),
    FOREIGN KEY (core_set_id) REFERENCES core_set(core_set_id),
    FOREIGN KEY (category_id) REFERENCES icf_category(category_id)
);