-- MySQL schemas
-- To import your schemas into your database, run:
-- `mysql -u username -p database < schema.sql` from the project directory
-- where username is your MySQL username

CREATE TABLE IF NOT EXISTS glassware (
  id TINYINT UNSIGNED NOT NULL,
  name TINYTEXT NULL,
  create_date DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";

CREATE TABLE IF NOT EXISTS categories (
  id TINYINT UNSIGNED NOT NULL,
  name TINYTEXT NULL,
  create_date DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";

CREATE TABLE IF NOT EXISTS availability (
  id TINYINT UNSIGNED NOT NULL,
  name TINYTEXT NULL,
  create_date DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";

CREATE TABLE IF NOT EXISTS styles (
  id TINYINT UNSIGNED NOT NULL,
  name TINYTEXT NULL,
  description TEXT NULL,
  category_id TINYINT UNSIGNED NULL,
  ibu_min TINYINT UNSIGNED NULL,
  ibu_max TINYINT UNSIGNED NULL,
  abv_min DECIMAL(3, 1) UNSIGNED NULL,
  abv_max DECIMAL(3, 1) UNSIGNED NULL,
  srm_min TINYINT UNSIGNED NULL,
  srm_max TINYINT UNSIGNED NULL,
  og_min DECIMAL(4, 3) UNSIGNED NULL,
  og_max DECIMAL(4, 3) UNSIGNED NULL,
  fg_min DECIMAL(4, 3) UNSIGNED NULL,
  fg_max DECIMAL(4, 3) UNSIGNED NULL,
  create_date DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";


CREATE TABLE IF NOT EXISTS beer (
  id CHAR(6) NOT NULL,
  name TINYTEXT NULL,
  description TEXT NULL,
  abv DECIMAL(3, 1) UNSIGNED NULL,
  ibu INT UNSIGNED NULL,
  glassware_id INT UNSIGNED NULL,
  style_id INT UNSIGNED NULL,
  is_organic CHAR(1) NULL,
  food_pairings TEXT NULL,
  original_gravity INT UNSIGNED NULL,
  labels_icon TINYTEXT NULL,
  labels_medium TINYTEXT NULL,
  labels_large TINYTEXT NULL,
  serving_temperature TINYTEXT NULL,
  serving_temperature_display TINYTEXT NULL,
  status TINYTEXT NULL,
  status_display TINYTEXT NULL,
  available_id INT UNSIGNED NULL,
  beer_variation_id TINYTEXT NULL,
  year YEAR(4) NULL,
  create_date DATETIME NULL,
  update_date DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";
