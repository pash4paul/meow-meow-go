CREATE user mrcat WITH ENCRYPTED PASSWORD 'hsA*uauQ6CH$Kw_w';
CREATE DATABASE mmgo OWNER mrcat;
\c mmgo
CREATE TABLE pages(url text, text_tsv tsvector);
CREATE INDEX on pages using gin(text_tsv);
ALTER TABLE pages OWNER TO mrcat;
