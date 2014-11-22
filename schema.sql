-- MySQL schemas
-- Keeping track of your MySQL schemas can help with automating adding tables
-- to your MySQL database. Simply add the table schema below and use the import
-- command to upload it to your database.

-- To import your schemas into your database, run:
-- `mysql -u <username> -p <database> < schema.sql` from the project directory
-- where <username> is your MySQL username and <database> is the MySQL
-- database of interest.

CREATE TABLE IF NOT EXISTS beers (
  id CHAR(6) NOT NULL,
  name TINYTEXT NULL,
  description TEXT NULL,
  abv DECIMAL(3, 1) UNSIGNED NULL,
  ibu INT UNSIGNED NULL,
  glasswareId INT UNSIGNED NULL,
  glass TEXT NULL,
  styleId INT UNSIGNED NULL,
  style TEXT NULL,
  isOrganic CHAR(1) NULL,
  foodPairings TEXT NULL,
  originalGravity INT UNSIGNED NULL,
  labels TEXT NULL,
  servingTemperature TINYTEXT NULL,
  servingTemperatureDisplay TINYTEXT NULL,
  status TINYTEXT NULL,
  statusDisplay TINYTEXT NULL,
  availableId INT UNSIGNED NULL,
  available TEXT NULL,
  beerVariationId TINYTEXT NULL,
  beerVariation TEXT NULL,
  year YEAR(4) NULL,
  createDate DATETIME NULL,
  updateDate DATETIME NULL,

  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = "utf8";
