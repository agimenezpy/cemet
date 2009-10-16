INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('Z', 'Resultado Preliminar', 'Sin control de calidad', false);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('C', 'Aprobación basta', 'Nivel 1 aprovado', true);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('S', 'Monitoreado', 'Niveles 1 y 2 aprobados', true);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('V', 'Verificado', 'Niveles 1, 2, y 3 aprobados', true);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('X', 'Rechazado/errorneo', 'Nivel 1 reprobado', true);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('Q', 'En duda', 'Nivel 1 aprovado, Nivel 2 o 3 reprobado', true);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('G', 'Subjectivamento bueno', 'Intervención subjetiva', false);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('B', 'Subjetivamente malo', 'Intervención subjetiva', false);
INSERT INTO calidad (codigo, descripcion, comentario, automatico)
        VALUES ('T', 'Virtual temperature could not be calculated', 'air temperature passing all QC', false);
