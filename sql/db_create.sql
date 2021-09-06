-- remove objects if they exist
CREATE DATABASE IF NOT EXISTS website;
DROP TABLE IF EXISTS website.articles;
DROP TRIGGER IF EXISTS website.update_publish;

CREATE TABLE website.articles (
    filename VARCHAR(25) PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    published boolean NOT NULL DEFAULT 0,
    publish_date DATE DEFAULT NULL,
    check((title IS NOT NULL) OR (published = 0))
);

-- trigger that sets publish date when publish changes to 1

DELIMITER $$

CREATE TRIGGER website.update_publish
    BEFORE UPDATE
    ON website.articles FOR EACH ROW
BEGIN
    SET NEW.publish_date = CURRENT_DATE();
END$$    

DELIMITER ;
