USE INSURIT;
DELIMITER //
CREATE FUNCTION auth (USR VARCHAR(20), PSWD VARCHAR(40))
RETURNS INTEGER
DETERMINISTIC
BEGIN
    DECLARE hashed VARCHAR(255);
    DECLARE count_matches INT;
    SET hashed = SHA2(LOWER(PSWD), 256);

    SELECT COUNT(*)
    INTO count_matches
    FROM INSURIT.SECRETS
    WHERE USERNAME = USR AND SECRET = hashed;

    IF count_matches > 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END //
DELIMITER ;
