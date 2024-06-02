-- @block users table
CREATE TABLE users (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);
-- @block photos table
CREATE TABLE photos (
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    photo_path VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username)
);
-- @block tags table
CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    FOREIGN KEY (username) REFERENCES users(username)
);
-- @block photos_tags table
CREATE TABLE photo_tags (
    photo_id INT,
    tag_id INT,
    PRIMARY KEY (photo_id, tag_id),
    FOREIGN KEY (photo_id) REFERENCES photos(photo_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);