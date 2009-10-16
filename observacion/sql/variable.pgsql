--
-- PostgreSQL database dump
--

SET client_encoding = 'LATIN1';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Data for Name: variable; Type: TABLE DATA; Schema: public; Owner: gisadm
--

COPY variable (codigo, descripcion, unidad_id, valor_inf, valor_sup) FROM stdin;
TD	Temperatura de punto de rocío	1	-67.78	32.22
RH	Humedad Relativa	2	0.00	100.00
P	Presión de la estación	4	568.00	1100.00
SLP	Presión a nivel del Mar	4	846.00	1100.00
PT3	Presión cambio en 3H	4	0.00	30.50
T	Temperatura del aire	1	-51.12	54.44
DD	Dirección del Viento	3	0.00	360.00
FF	Velocidad del Viento	5	0.00	463.00
U	Componente U del viento	9	0.00	0.00
V	Componente V del viento	9	0.00	0.00
PCP	Presipitación Acumulada	7	0.00	111.76
SOILMP	Humedad del suelo %	2	0.00	100.00
SOILT	Temperatura del suelo	1	-40.00	65.56
SST	Temperatura a nivel del mar	1	-2.00	40.00
\.


--
-- PostgreSQL database dump complete
--

