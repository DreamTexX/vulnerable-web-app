CREATE TABLE `accounts` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `email` TEXT UNIQUE NOT NULL,
    `username` TEXT UNIQUE NOT NULL,
    `password` TEXT NOT NULL
);

CREATE TABLE `posts` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `author_id` INT NOT NULL REFERENCES `accounts`(`id`),
    `content` TEXT NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO `accounts`
    (`id`, `email`, `username`, `password`)
VALUES
    (1, 'user1', 'Cool User #1', '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90'),
    (2, 'user2', 'Cool User #2', '6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3');

INSERT INTO `posts`
    (`id`, `author_id`, `content`, `created_at`)
VALUES
    (1, 1, 'Hey, das ist mein erster Chrip!', '2022-11-20 12:04:43'),
    (2, 1, 'Update: das hier ist mein zweiter Chirp!', '2022-11-25 17:23:12'),
    (3, 2, 'Hey ich bin jetzt auch bei Chirp!', '2022-12-07 10:45:47');