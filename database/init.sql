CREATE TABLE `accounts` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `email` TEXT UNIQUE NOT NULL,
    `password` TEXT UNIQUE NOT NULL
);

CREATE TABLE `posts` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `author_id` INT NOT NULL REFERENCES `accounts`(`id`),
    `content` TEXT NOT NULL
);