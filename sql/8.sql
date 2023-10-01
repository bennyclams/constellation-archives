use `constellation_archives`;

CREATE TABLE IF NOT EXISTS `planets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `system` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `gravity` float NOT NULL,
  `temperature` varchar(255) NOT NULL,
  `atmosphere` varchar(255) NOT NULL,
  `magnetosphere` varchar(255) NOT NULL,
  `fauna` int(11) NOT NULL,
  `flora` int(11) NOT NULL,
  `water` varchar(255) NOT NULL,
  `resources` JSON NOT NULL,
  `traits` JSON NOT NULL,
  `moons` JSON NOT NULL,
  `description` TEXT NOT NULL,
  `submitter` varchar(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;