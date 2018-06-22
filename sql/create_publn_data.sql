CREATE TABLE app_names (
  name VARCHAR(255) PRIMARY KEY
) ENGINE=Mroonga DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='default_tokenizer "TokenDelimit"';

CREATE TABLE inv_names (
  name VARCHAR(255) PRIMARY KEY
) ENGINE=Mroonga DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='default_tokenizer "TokenDelimit"';

CREATE TABLE ator_names (
  name VARCHAR(255) PRIMARY KEY
) ENGINE=Mroonga DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='default_tokenizer "TokenDelimit"';

CREATE TABLE ipc_tags (
  name VARCHAR(255) PRIMARY KEY
) ENGINE=Mroonga DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='default_tokenizer "TokenDelimit"';

CREATE TABLE fi_tags (
  name VARCHAR(255) PRIMARY KEY
) ENGINE=Mroonga DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='default_tokenizer "TokenDelimit"';

CREATE TABLE publn_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  appln_nr VARCHAR(15) UNIQUE,
  type VARCHAR(5),
  publn_nr VARCHAR(15),
  reg_nr VARCHAR(15),
  filing_date DATE,
  filing_year VARCHAR(4),
  filing_month VARCHAR(2),
  pub_date DATE,
  pub_year VARCHAR(4),
  pub_month VARCHAR(2),
  reg_date DATE,
  reg_year VARCHAR(4),
  reg_month VARCHAR(2),
  nb_claim INTEGER,
  applicants TEXT COMMENT 'flags "COLUMN_VECTOR", type "app_names"',
  attorneys TEXT COMMENT 'flags "COLUMN_VECTOR", type "ator_names"',
  inventors TEXT COMMENT 'flags "COLUMN_VECTOR", type "inv_names"',
  clsf TEXT COMMENT 'flags "COLUMN_VECTOR", type "ipc_tags"',
  fi TEXT COMMENT 'flags "COLUMN_VECTOR", type "fi_tags"',
  title TEXT,
  description LONGTEXT,
  claims LONGTEXT,
  abstract TEXT,
  FULLTEXT INDEX app_index(applicants) COMMENT 'table "app_names"',
  FULLTEXT INDEX att_index(attorneys) COMMENT 'table "ator_names"',
  FULLTEXT INDEX inv_index(inventors) COMMENT 'table "inv_names"',
  FULLTEXT INDEX clsf_index(clsf) COMMENT 'table "ipc_tags"',
  FULLTEXT INDEX fi_index(fi) COMMENT 'table "fi_tags"',
  FULLTEXT INDEX (title),
  FULLTEXT INDEX (description),
  FULLTEXT INDEX (claims),
  FULLTEXT INDEX (abstract)
) ENGINE = Mroonga DEFAULT CHARSET utf8;

CREATE TABLE publn_error (
  xml_path TEXT,
  message TEXT
)
