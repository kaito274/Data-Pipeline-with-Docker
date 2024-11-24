USE kafkapipeline;
DROP TABLE IF EXISTS kafkapipeline.fakerdata;
CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  ssn TEXT PRIMARY KEY,
  name TEXT,
  address TEXT,
  year INT,
  city TEXT,
  credit_card_number TEXT,
  credit_card_provider TEXT,
  email TEXT,
  country TEXT,
  phone_number TEXT
);
