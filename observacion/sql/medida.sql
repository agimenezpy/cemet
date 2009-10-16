ALTER TABLE medida DROP COLUMN id;
ALTER TABLE medida ADD CONSTRAINT PRIMARY KEY (sensor_id, tiempo);
CREATE INDEX sens_temp ON medida (sensor_id, tiempo ASC);