CREATE DATABASE IF NOT EXISTS hbnb_evaluation;
USE hbnb_evaluation;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS amenities (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS places (
    id VARCHAR(36) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(36) NOT NULL,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT uq_review_user_place UNIQUE (user_id, place_id),
    CONSTRAINT chk_review_rating CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$kgVuE6DCVUDrTZvxlqI/P.0dh/m4G0POvMADJhFASKXoPvvuy6ZtK', TRUE, NOW(), NOW());

INSERT INTO amenities (id, name, created_at, updated_at) VALUES (UUID(), 'WiFi', NOW(), NOW());
INSERT INTO amenities (id, name, created_at, updated_at) VALUES (UUID(), 'Swimming Pool', NOW(), NOW());
INSERT INTO amenities (id, name, created_at, updated_at) VALUES (UUID(), 'Air Conditioning', NOW(), NOW());
