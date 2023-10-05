use `constellation_archives`;

-- I don't like storing settings like this because there's just one row in the table,
-- but not sure where else to put this...
CREATE TABLE IF NOT EXISTS `index_settings` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `main_text` TEXT NOT NULL,
    `banner_text` TEXT NOT NULL,
    `banner_type` VARCHAR(255) NOT NULL,
    `banner_enabled` TINYINT(1) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;