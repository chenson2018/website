-- remove objects if they exist
CREATE DATABASE IF NOT EXISTS website;
DROP TABLE IF EXISTS website.articles;

CREATE TABLE website.articles (
    filename VARCHAR(25) PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    published boolean NOT NULL DEFAULT 0,
    publish_date DATE DEFAULT NULL,
    check((title IS NOT NULL) OR (published = 0))
);


