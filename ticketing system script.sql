DROP DATABASE IF EXISTS ticketing_system;

CREATE DATABASE ticketing_system;
USE ticketing_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role ENUM('admin', 'technician') NOT NULL
);

CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('open', 'in_progress', 'resolved') DEFAULT 'open',
    created_by INT,
    assigned_to INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

INSERT INTO users (name, email, role)
VALUES 
('Alice', 'alice@example.com', 'admin'),
('Bob', 'bob@example.com', 'technician'),
('Charlie', 'charlie@example.com', 'technician');

INSERT INTO tickets (title, description, status, created_by, assigned_to)
VALUES 
('Fix printer issue', 'Printer in lab is jammed', 'open', 1, 2),
('Reset student password', 'Student forgot login', 'in_progress', 1, 3);
