ALTER TABLE medida ADD CHECK (qc_desc IN ('Z','C','S','V','X','Q','G','B'));
ALTER TABLE medida ALTER COLUMN qc_desc SET DEFAULT 'Z';
ALTER TABLE medida ALTER COLUMN tiempo TYPE timestamp without time zone;
ALTER TABLE medida ALTER COLUMN valor TYPE REAL;
ALTER TABLE medida ADD FOREIGN KEY (estacion_id, variable_id) REFERENCES estacion_variable(estacion_id, variable_id);
ALTER TABLE medida ADD CONSTRAINT UNIQUE (tiempo, estacion_id, variable_id, valor);
CREATE INDEX medida_tiempo_idx ON medida USING btree (tiempo)

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