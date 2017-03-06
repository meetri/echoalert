-- Table: echoalert.accounts

-- DROP TABLE echoalert.accounts;

CREATE TABLE echoalert.accounts
(
    id integer NOT NULL,
    echo_username character varying(64) COLLATE pg_catalog."default",
    echo_password character varying(32) COLLATE pg_catalog."default",
    created_ts timestamp with time zone,
    modified_ts timestamp with time zone,
    last_updated timestamp with time zone,
    last_checked timestamp with time zone,
    notification_email character varying(128) COLLATE pg_catalog."default",
    notification_sms character varying(128) COLLATE pg_catalog."default",
    echo_site character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT student_grades_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE echoalert.accounts
    OWNER to postgres;

-- Table: echoalert.grade_summary

-- DROP TABLE echoalert.grade_summary;

CREATE TABLE echoalert.grade_summary
(
    id integer NOT NULL DEFAULT nextval('echoalert.grade_summary_id_seq'::regclass),
    account_id integer,
    created_ts timestamp with time zone,
    co double precision,
    ag double precision,
    progress_all double precision,
    kn double precision,
    course character varying(128) COLLATE pg_catalog."default",
    score double precision,
    progress_gradable double precision,
    oral double precision,
    wr double precision,
    groupset bigint,
    CONSTRAINT grade_summary_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE echoalert.grade_summary
    OWNER to postgres;

-- Index: gs_accountid_index

-- DROP INDEX echoalert.gs_accountid_index;

CREATE INDEX gs_accountid_index
    ON echoalert.grade_summary USING btree
    (account_id)
    TABLESPACE pg_default;

-- Index: gs_groupset_index

-- DROP INDEX echoalert.gs_groupset_index;

CREATE INDEX gs_groupset_index
    ON echoalert.grade_summary USING btree
    (groupset DESC)
    TABLESPACE pg_default;
