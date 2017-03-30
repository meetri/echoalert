--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

-- Started on 2017-03-30 09:38:48 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2176 (class 1262 OID 16384)
-- Name: echoalert; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE echoalert WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE echoalert OWNER TO postgres;

\connect echoalert

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 8 (class 2615 OID 16385)
-- Name: echoalert; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA echoalert;


ALTER SCHEMA echoalert OWNER TO postgres;

--
-- TOC entry 1 (class 3079 OID 12393)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2178 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = echoalert, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 186 (class 1259 OID 16386)
-- Name: accounts; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE accounts (
    id integer NOT NULL,
    echo_username character varying(64),
    echo_password character varying(32),
    created_ts timestamp with time zone,
    modified_ts timestamp with time zone,
    last_updated timestamp with time zone,
    last_checked timestamp with time zone,
    notification_email character varying(128),
    notification_sms character varying(128),
    echo_site character varying(255),
    enabled boolean
);


ALTER TABLE accounts OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 24647)
-- Name: assignments; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE assignments (
    id integer NOT NULL,
    hash character varying(32),
    account_id integer,
    course_id integer,
    assignment_type integer,
    title text,
    due_date timestamp with time zone,
    created_ts timestamp with time zone,
    completed boolean,
    due character varying(64)
);


ALTER TABLE assignments OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 24645)
-- Name: assignments_id_seq; Type: SEQUENCE; Schema: echoalert; Owner: postgres
--

CREATE SEQUENCE assignments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE assignments_id_seq OWNER TO postgres;

--
-- TOC entry 2179 (class 0 OID 0)
-- Dependencies: 193
-- Name: assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: echoalert; Owner: postgres
--

ALTER SEQUENCE assignments_id_seq OWNED BY assignments.id;


--
-- TOC entry 187 (class 1259 OID 16397)
-- Name: courses; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE courses (
    id integer NOT NULL,
    account_id integer,
    status integer,
    created_ts timestamp with time zone,
    course_name character varying(128),
    course_term character varying(128)
);


ALTER TABLE courses OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 16400)
-- Name: courses_id_seq; Type: SEQUENCE; Schema: echoalert; Owner: postgres
--

CREATE SEQUENCE courses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE courses_id_seq OWNER TO postgres;

--
-- TOC entry 2180 (class 0 OID 0)
-- Dependencies: 188
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: echoalert; Owner: postgres
--

ALTER SEQUENCE courses_id_seq OWNED BY courses.id;


--
-- TOC entry 189 (class 1259 OID 16402)
-- Name: grade_summary; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE grade_summary (
    id integer NOT NULL,
    account_id integer,
    course_id integer,
    created_ts timestamp with time zone,
    progress_all double precision,
    progress_gradable double precision,
    score double precision,
    oral double precision,
    co double precision,
    ag double precision,
    kn double precision,
    wr double precision
);


ALTER TABLE grade_summary OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 16405)
-- Name: grade_summary_id_seq; Type: SEQUENCE; Schema: echoalert; Owner: postgres
--

CREATE SEQUENCE grade_summary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE grade_summary_id_seq OWNER TO postgres;

--
-- TOC entry 2181 (class 0 OID 0)
-- Dependencies: 190
-- Name: grade_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: echoalert; Owner: postgres
--

ALTER SEQUENCE grade_summary_id_seq OWNED BY grade_summary.id;


--
-- TOC entry 191 (class 1259 OID 16407)
-- Name: notifications; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE notifications (
    id integer NOT NULL,
    account_id integer NOT NULL,
    notification_type integer NOT NULL,
    status integer,
    status_message character varying(64),
    sent_ts timestamp with time zone,
    created_ts timestamp with time zone
);


ALTER TABLE notifications OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 16410)
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: echoalert; Owner: postgres
--

CREATE SEQUENCE notifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notifications_id_seq OWNER TO postgres;

--
-- TOC entry 2182 (class 0 OID 0)
-- Dependencies: 192
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: echoalert; Owner: postgres
--

ALTER SEQUENCE notifications_id_seq OWNED BY notifications.id;


--
-- TOC entry 196 (class 1259 OID 24734)
-- Name: notify_accounts; Type: TABLE; Schema: echoalert; Owner: postgres
--

CREATE TABLE notify_accounts (
    id integer NOT NULL,
    account_id integer NOT NULL,
    sms_name character varying(32) NOT NULL,
    sms_contact character varying(12) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE notify_accounts OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 24732)
-- Name: notify_accounts_id_seq; Type: SEQUENCE; Schema: echoalert; Owner: postgres
--

CREATE SEQUENCE notify_accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notify_accounts_id_seq OWNER TO postgres;

--
-- TOC entry 2183 (class 0 OID 0)
-- Dependencies: 195
-- Name: notify_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: echoalert; Owner: postgres
--

ALTER SEQUENCE notify_accounts_id_seq OWNED BY notify_accounts.id;


--
-- TOC entry 2039 (class 2604 OID 24650)
-- Name: assignments id; Type: DEFAULT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY assignments ALTER COLUMN id SET DEFAULT nextval('assignments_id_seq'::regclass);


--
-- TOC entry 2036 (class 2604 OID 16429)
-- Name: courses id; Type: DEFAULT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY courses ALTER COLUMN id SET DEFAULT nextval('courses_id_seq'::regclass);


--
-- TOC entry 2037 (class 2604 OID 16430)
-- Name: grade_summary id; Type: DEFAULT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY grade_summary ALTER COLUMN id SET DEFAULT nextval('grade_summary_id_seq'::regclass);


--
-- TOC entry 2038 (class 2604 OID 16431)
-- Name: notifications id; Type: DEFAULT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY notifications ALTER COLUMN id SET DEFAULT nextval('notifications_id_seq'::regclass);


--
-- TOC entry 2040 (class 2604 OID 24737)
-- Name: notify_accounts id; Type: DEFAULT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY notify_accounts ALTER COLUMN id SET DEFAULT nextval('notify_accounts_id_seq'::regclass);


--
-- TOC entry 2052 (class 2606 OID 24655)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 2044 (class 2606 OID 16419)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- TOC entry 2046 (class 2606 OID 16421)
-- Name: grade_summary grade_summary_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY grade_summary
    ADD CONSTRAINT grade_summary_pkey PRIMARY KEY (id);


--
-- TOC entry 2050 (class 2606 OID 16423)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- TOC entry 2054 (class 2606 OID 24739)
-- Name: notify_accounts notify_accounts_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY notify_accounts
    ADD CONSTRAINT notify_accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 2042 (class 2606 OID 16425)
-- Name: accounts student_grades_pkey; Type: CONSTRAINT; Schema: echoalert; Owner: postgres
--

ALTER TABLE ONLY accounts
    ADD CONSTRAINT student_grades_pkey PRIMARY KEY (id);


--
-- TOC entry 2047 (class 1259 OID 16426)
-- Name: gs_accountid_index; Type: INDEX; Schema: echoalert; Owner: postgres
--

CREATE INDEX gs_accountid_index ON grade_summary USING btree (account_id);


--
-- TOC entry 2048 (class 1259 OID 16427)
-- Name: gs_createdts_index; Type: INDEX; Schema: echoalert; Owner: postgres
--

CREATE INDEX gs_createdts_index ON grade_summary USING btree (created_ts DESC);


-- Completed on 2017-03-30 09:39:10 PDT

--
-- PostgreSQL database dump complete
--

