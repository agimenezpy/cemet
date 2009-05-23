ALTER TABLE medida ADD CHECK (qc_desc IN ('Z','C','S','V','X','Q','G','B'));
ALTER TABLE medida ALTER COLUMN qc_desc SET DEFAULT 'Z';
ALTER TABLE medida ALTER COLUMN tiempo TYPE timestamp without time zone;
ALTER TABLE medida ALTER COLUMN valor TYPE REAL;
ALTER TABLE medida ADD FOREIGN KEY (estacion_id, variable_id) REFERENCES estacion_variable(estacion_id, variable_id);
ALTER TABLE medida ADD CONSTRAINT UNIQUE (tiempo, estacion_id, variable_id, valor);
CREATE INDEX medida_tiempo_idx ON medida USING btree (tiempo)