--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_table_access_method = heap;

--
-- Name: ban; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ban (
    "IP" text NOT NULL,
    "timestamp" bigint NOT NULL,
    reason text NOT NULL
);


--
-- Name: ips; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ips (
    "IP" text NOT NULL,
    whitelisted boolean NOT NULL
);


--
-- Name: log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.log (
    "ID" integer NOT NULL,
    service text NOT NULL,
    "IP" text NOT NULL,
    "timestamp" bigint NOT NULL,
    data text NOT NULL
);


--
-- Name: log_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."log_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: log_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."log_ID_seq" OWNED BY public.log."ID";


--
-- Name: log ID; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log ALTER COLUMN "ID" SET DEFAULT nextval('public."log_ID_seq"'::regclass);


--
-- Name: ban ban_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ban
    ADD CONSTRAINT ban_pkey PRIMARY KEY ("IP");


--
-- Name: ips ips_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ips
    ADD CONSTRAINT ips_pkey PRIMARY KEY ("IP");


--
-- Name: log log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT log_pkey PRIMARY KEY ("ID");


--
-- Name: ban ban_IP_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ban
    ADD CONSTRAINT "ban_IP_fkey" FOREIGN KEY ("IP") REFERENCES public.ips("IP");


--
-- Name: log log_IP_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log
    ADD CONSTRAINT "log_IP_fkey" FOREIGN KEY ("IP") REFERENCES public.ips("IP");


--
-- PostgreSQL database dump complete
--

