ALTER TABLE medida DROP COLUMN id;
ALTER TABLE medida ALTER COLUMN tiempo TYPE timestamp without time zone;
ALTER TABLE medida ADD PRIMARY KEY (tiempo, medidor_id);
CREATE INDEX medida_tiempo_medidor_id ON medida (tiempo, medidor_id);