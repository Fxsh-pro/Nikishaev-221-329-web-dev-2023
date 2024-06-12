-- Create table for genres
CREATE TABLE if not exists genres (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL
);

-- Create table for book covers
CREATE TABLE if not exists book_covers (
                             id INT AUTO_INCREMENT PRIMARY KEY,
                             file_name VARCHAR(255) NOT NULL,
                             mime_type VARCHAR(255) NOT NULL,
                             md5_hash VARCHAR(255) NOT NULL
);

-- Create table for books
CREATE TABLE if not exists books (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(255) NOT NULL,
                       description TEXT NOT NULL,
                       year int NOT NULL,
                       publisher VARCHAR(255) NOT NULL,
                       author VARCHAR(255) NOT NULL,
                       pages INT NOT NULL,
                       cover_id INT,
                       FOREIGN KEY (cover_id) REFERENCES book_covers(id) ON DELETE CASCADE
);

-- Create table for book-genre relationship
CREATE TABLE if not exists book_genres (
                             book_id INT,
                             genre_id INT,
                             PRIMARY KEY (book_id, genre_id),
                             FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                             FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

CREATE TABLE roles (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       description TEXT NOT NULL
);


-- Create table for users
CREATE TABLE users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       login VARCHAR(255) NOT NULL,
                       password_hash VARCHAR(255) NOT NULL,
                       last_name VARCHAR(255) NOT NULL,
                       first_name VARCHAR(255) NOT NULL,
                       middle_name VARCHAR(255),
                       role_id INT NOT NULL,
                       FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Create table for roles
CREATE TABLE if not exists roles  (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       description TEXT NOT NULL
);

-- Populate roles table
INSERT INTO roles (name, description) VALUES
                                          ('admin', 'Superuser with full access'),
                                          ('moderator', 'Can edit book data and moderate reviews'),
                                          ('user', 'Can leave reviews');

-- Create table for reviews
CREATE TABLE if not exists reviews (
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         book_id INT NOT NULL,
                         user_id INT NOT NULL,
                         rating INT NOT NULL,
                         text TEXT NOT NULL,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                         FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
