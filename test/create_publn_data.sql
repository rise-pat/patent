/*CREATE TABLE app_names (
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
*/
CREATE TABLE publn_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  appln_nr VARCHAR(15) UNIQUE,
  publn_nr VARCHAR(15),
  reg_nr VARCHAR(15),
  filing_date DATE,
  pub_date DATE,
  reg_date DATE,
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
  FULLTEXT INDEX (applicants) COMMENT 'table "app_names"',
  FULLTEXT INDEX (attorneys) COMMENT 'table "ator_names"',
  FULLTEXT INDEX (inventors) COMMENT 'table "inv_names"',
  FULLTEXT INDEX (clsf) COMMENT 'table "ipc_tags"',
  FULLTEXT INDEX (fi) COMMENT 'table "fi_tags"',
  FULLTEXT INDEX (title),
  FULLTEXT INDEX (description),
  FULLTEXT INDEX (claims),
  FULLTEXT INDEX (abstract)
) ENGINE = Mroonga DEFAULT CHARSET utf8;
