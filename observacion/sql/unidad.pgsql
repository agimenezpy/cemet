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
-- Name: unidad_medida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gisadm
--

SELECT pg_catalog.setval('unidad_medida_id_seq', 9, true);


--
-- Data for Name: unidad_medida; Type: TABLE DATA; Schema: public; Owner: gisadm
--

COPY unidad_medida (id, descripcion, notacion) FROM stdin;
1	Grados Celcius	ºC
2	Porcentaje	%
3	Grados	º
4	HectoPascal	hP
5	Kilometros por hora	km/h
6	Kilometros	km
7	Centímetros	cm
8	Metros	m
9	Unidad	u
\.


--
-- PostgreSQL database dump complete
--

