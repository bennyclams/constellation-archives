use `constellation_archives`;

ALTER TABLE `items` ADD `submitter` varchar(255) NOT NULL DEFAULT 'Anonymous' AFTER `categories`;
ALTER TABLE `item_types` ADD `submitter` varchar(255) NOT NULL DEFAULT 'Anonymous' AFTER `name`;
ALTER TABLE `categories` ADD `submitter` varchar(255) NOT NULL DEFAULT 'Anonymous' AFTER `thumbnail`;

ALTER TABLE `items` ADD FOREIGN KEY (`submitter`) REFERENCES `users`(`username`);
ALTER TABLE `item_types` ADD FOREIGN KEY (`submitter`) REFERENCES `users`(`username`);
ALTER TABLE `categories` ADD FOREIGN KEY (`submitter`) REFERENCES `users`(`username`);
