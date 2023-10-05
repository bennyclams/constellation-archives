use `constellation_archives`;

ALTER TABLE `users` ADD `last_login` DATETIME DEFAULT NULL AFTER `updated_at`;