CREATE TABLE log_dni_values(
    log_datetime TIMESTAMP NOT NULL,
    dni_id INT NOT NULL,
    dni_value FLOAT,
    CONSTRAINT log_dni_pk PRIMARY KEY (log_datetime, dni_id)
);

CREATE OR REPLACE FUNCTION add_dni_values(
    p_log_datetime TIMESTAMP,
    p_dni_id INT,
    p_dni_value FLOAT
) RETURNS void
AS $$
BEGIN
INSERT INTO log_dni_values(
    log_datetime,
    dni_id,
    dni_value
) VALUES (
    p_log_datetime,
    p_dni_id,
    p_dni_value
);
END;
$$ LANGUAGE plpgsql;