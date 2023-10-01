use `constellation_archives`;

CREATE TABLE IF NOT EXISTS `systems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `catalogue_id` varchar(255) NOT NULL,
  `class` varchar(255) NOT NULL,
  `temperature` varchar(255) NOT NULL,
  `mass` varchar(255) NOT NULL,
  `radius` varchar(255) NOT NULL,
  `magnitude` varchar(255) NOT NULL,
  `planet_count` int(11) NOT NULL,
  `moon_count` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `faction` varchar(255) NOT NULL DEFAULT 'None',
  `description` TEXT NOT NULL,
  `submitter` varchar(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;