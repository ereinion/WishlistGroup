DROP DATABASE IF EXISTS lister;
CREATE DATABASE lister;
\c lister;
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
                    email VARCHAR(32) NOT NULL,
                    PRIMARY KEY(email),
                    firstName VARCHAR(32) NOT NULL DEFAULT 'John',
                    lastName VARCHAR(32) NOT NULL DEFAULT 'Doe',
                    password VARCHAR(64) NOT NULL
                    );
                    
DROP TABLE IF EXISTS most_wanted;
CREATE TABLE most_wanted (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    item_name VARCHAR(32) NOT NULL
                    );
                    
DROP TABLE IF EXISTS join_date;
CREATE TABLE user_join_date (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    date_joined VARCHAR(32) NOT NULL
                    );
    
DROP TABLE IF EXISTS date_of_birth;
CREATE TABLE user_date_of_birth (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    birth_date VARCHAR(32) NOT NULL
                    );                    
                    
DROP TABLE IF EXISTS user_gender;
CREATE TABLE user_gender (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    gender VARCHAR(32) NOT NULL
                    );
                    
DROP TABLE IF EXISTS phone_number;
CREATE TABLE user_phone_number (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    phone_number VARCHAR(32) NOT NULL
                    );
                    
DROP TABLE IF EXISTS user_address;
CREATE TABLE user_address (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    address VARCHAR(32) NOT NULL
                    );

DROP TABLE IF EXISTS items;
CREATE TABLE items (
                    id serial NOT NULL,
                    PRIMARY KEY(id),
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    item_name VARCHAR(32) NOT NULL,
                    item_price int NOT NULL
                    );
                    
DROP TABLE IF EXISTS links;
CREATE TABLE links (
                    item_id INT REFERENCES items (id) NOT NULL,
                    url VARCHAR(144) NOT NULL
                    );

DROP TABLE IF EXISTS friends_with;
CREATE TABLE  friends_with (
                    user_email VARCHAR(32) REFERENCES users (email) NOT NULL,
                    friend_email VARCHAR(32) REFERENCES users (email) NOT NULL
                    );