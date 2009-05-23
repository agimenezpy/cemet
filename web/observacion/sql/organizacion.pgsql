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
-- Name: organizacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gisadm
--

SELECT pg_catalog.setval('organizacion_id_seq', 1, true);


--
-- Data for Name: organizacion; Type: TABLE DATA; Schema: public; Owner: gisadm
--

COPY organizacion (id, nombre, siglas, pais_id) FROM stdin;
1	Dirección Nacional de Aeronáutica Civil	DINAC	PY
\.


--
-- PostgreSQL database dump complete
--

