BEGIN;
/**
 * Procedimientos para efectuar control de calidad de acuerdo a la especificación
 * MADIS Meteorological and Hidrological Surface Quality Control
 */
CREATE OR REPLACE FUNCTION validity_check() RETURNS trigger AS $validity_check$
DECLARE
    rec RECORD;
BEGIN
    SELECT INTO rec valor_inf, valor_sup FROM "variable" WHERE codigo = NEW.variable_id;
    IF rec.valor_inf > NEW.valor OR rec.valor_sup < NEW.valor
    THEN
        -- X - Rejected/erroneous
        NEW.qc_desc := 'X';
        -- Validity Check
        --NEW.qc_aplicado := 2;
        -- Master Check y Validity Check failed
        --NEW.qc_result := 1 + 2;
    ELSE
        -- C - Coarse pass
        NEW.qc_desc := 'C';
        -- Master Check y Validity Check
        --NEW.qc_aplicado := 1 + 2;
        --NEW.qc_result := 0;
    END IF;
    RETURN NEW;
END;
$validity_check$ LANGUAGE plpgsql;

CREATE TRIGGER validity_check BEFORE INSERT OR UPDATE ON medida FOR EACH ROW EXECUTE PROCEDURE validity_check();
END;