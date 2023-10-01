use `constellation_archives`;

CREATE TABLE IF NOT EXISTS `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `item_type` varchar(255) NOT NULL,
  `description` TEXT NOT NULL,
  `images` JSON NOT NULL,
  `categories` JSON NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `items_item_type_foreign` (`item_type`),
  CONSTRAINT `items_item_type_foreign` FOREIGN KEY (`item_type`) REFERENCES `item_types` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;