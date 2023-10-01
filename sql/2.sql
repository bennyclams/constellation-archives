USE `constellation_archives`;
ALTER TABLE `users` ADD `roles` varchar(255) NOT NULL DEFAULT 'user' AFTER `password`;