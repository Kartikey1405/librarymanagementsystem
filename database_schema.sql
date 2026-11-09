CREATE DATABASE IF NOT EXISTS library_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE library_db;


-- 1. USERS TABLE

CREATE TABLE IF NOT EXISTS Users (

    user_id VARCHAR(12) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    password_hash VARCHAR(255) NOT NULL,

    role ENUM(
        'STUDENT',
        'TEACHER',
        'LIBRARIAN'
    ) NOT NULL DEFAULT 'STUDENT',

    joining_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB;


-- 2. BOOKS TABLE

CREATE TABLE IF NOT EXISTS Books (

    book_id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(60),
    publisher VARCHAR(100),

    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_book_copies CHECK (
        total_copies >= 0
        AND available_copies >= 0
        AND available_copies <= total_copies
    )

) ENGINE=InnoDB;


-- 3. ISSUE REQUESTS TABLE

CREATE TABLE IF NOT EXISTS Issue_Requests (

    request_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id VARCHAR(12) NOT NULL,
    book_id INT NOT NULL,

    request_date DATE NOT NULL,

    status ENUM(
        'PENDING',
        'APPROVED',
        'REJECTED',
        'ISSUED',
        'CANCELLED'
    ) NOT NULL DEFAULT 'PENDING',

    remarks VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

    FOREIGN KEY (book_id)
        REFERENCES Books(book_id)

) ENGINE=InnoDB;


-- 4. ISSUE RECORDS TABLE

CREATE TABLE IF NOT EXISTS Issue_Records (

    issue_id INT AUTO_INCREMENT PRIMARY KEY,

    request_id INT UNIQUE,

    user_id VARCHAR(12) NOT NULL,
    book_id INT NOT NULL,

    issue_date DATE NOT NULL,

    loan_days INT NOT NULL DEFAULT 7,

    due_date DATE NOT NULL,

    return_date DATE,

    status ENUM(
        'ISSUED',
        'RETURNED'
    ) NOT NULL DEFAULT 'ISSUED',

    return_condition ENUM(
        'GOOD',
        'DAMAGED'
    ),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id)
        REFERENCES Issue_Requests(request_id),

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

    FOREIGN KEY (book_id)
        REFERENCES Books(book_id),

    CONSTRAINT chk_loan_days CHECK (
        loan_days IN (7, 15)
    ),

    CONSTRAINT chk_return_state CHECK (
        (status = 'ISSUED' AND return_date IS NULL)
        OR
        (status = 'RETURNED' AND return_date IS NOT NULL)
    )

) ENGINE=InnoDB;


-- 5. FINES TABLE

CREATE TABLE IF NOT EXISTS Fines (

    fine_id INT AUTO_INCREMENT PRIMARY KEY,

    issue_id INT NOT NULL,

    fine_type ENUM(
        'LATE',
        'DAMAGE'
    ) NOT NULL,

    fine_amount DECIMAL(10,2) NOT NULL,

    fine_date DATE NOT NULL,

    payment_status ENUM(
        'PENDING',
        'PAID'
    ) NOT NULL DEFAULT 'PENDING',

    payment_date DATE,

    remarks VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (issue_id)
        REFERENCES Issue_Records(issue_id),

    CONSTRAINT chk_fine_amount CHECK (
        fine_amount > 0
    ),

    CONSTRAINT chk_payment_state CHECK (
        (payment_status = 'PENDING' AND payment_date IS NULL)
        OR
        (payment_status = 'PAID' AND payment_date IS NOT NULL)
    )

) ENGINE=InnoDB;