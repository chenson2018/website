DROP TRIGGER IF EXISTS website.update_publish;

-- trigger that sets publish date when publish changes to 1

DELIMITER $$

CREATE TRIGGER website.update_publish
    BEFORE UPDATE
    ON website.articles FOR EACH ROW
BEGIN
    IF OLD.published = 0 AND NEW.published = 1 THEN
    SET NEW.publish_date = CURRENT_DATE();
    END IF;
END$$    

DELIMITER ;
