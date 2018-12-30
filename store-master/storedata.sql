CREATE DATABASE store;
USE store;

CREATE TABLE categories(
name VARCHAR(30) UNIQUE,
id INT AUTO_INCREMENT UNIQUE,
PRIMARY KEY (id)
);

CREATE TABLE products(
id INT AUTO_INCREMENT,
title VARCHAR(30) UNIQUE,
description VARCHAR(500),
img_url VARCHAR(100),
price INT,
category VARCHAR(30),
favorite ENUM("0","1"),
PRIMARY KEY (id)
);