ROLLBACK;
BEGIN;

CREATE TYPE age_rating_enum AS ENUM ('0+', '6+', '12+', '16+', '18+');
								-------------------
								--  DELETE BASE  --
								-------------------

DROP TABLE IF EXISTS payments_data.cheque_book CASCADE;
DROP TABLE IF EXISTS payments_data.cheque_contract CASCADE;
DROP TABLE IF EXISTS books_data.author_book CASCADE;
DROP TABLE IF EXISTS books_data.book_genre CASCADE;
DROP TABLE IF EXISTS subscribes_data.subscribe_book CASCADE;
DROP TABLE IF EXISTS books_data.user_book CASCADE;
DROP TABLE IF EXISTS books_data.reviews CASCADE;
DROP TABLE IF EXISTS books_data.books_changeable CASCADE;
DROP TABLE IF EXISTS books_data.books CASCADE;
DROP TABLE IF EXISTS books_data.authors CASCADE;
DROP TABLE IF EXISTS clients.users CASCADE;
DROP TABLE IF EXISTS clients.organisations CASCADE;
DROP TABLE IF EXISTS clients.personal_data CASCADE;
DROP TABLE IF EXISTS payments_data.contracts CASCADE;
DROP TABLE IF EXISTS payments_data.cheques CASCADE;
DROP TABLE IF EXISTS subscribes_data.subscribe_types CASCADE;
DROP TABLE IF EXISTS books_data.genres CASCADE;
DROP TABLE IF EXISTS books_data.languages CASCADE;
DROP TABLE IF EXISTS books_data.publishers CASCADE;
							
								-------------------
								-- CREATE SHEMAS --
								-------------------
CREATE SCHEMA books_data;
CREATE SCHEMA subscribes_data;
CREATE SCHEMA payments_data;
CREATE SCHEMA clients;
CREATE SCHEMA logs;

								-------------------
								-- CREATE TABLES --
								-------------------

-- books_data --
CREATE TABLE books_data.languages (
  language_id 				smallint 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,title 					varchar(32) 		UNIQUE NOT NULL
)
;


CREATE TABLE books_data.publishers (
  publisher_id 				smallint 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,"name" 					varchar(64) 		UNIQUE NOT NULL
  ,"link"					varchar(256) 		NOT NULL
)
;

CREATE TABLE books_data.authors (
  author_id					integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,author_name 				varchar(256) 		NOT NULL
  ,author_info				varchar(1024)
  ,created_at 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
)
;

CREATE TABLE books_data.genres (
  genre_id					smallint 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,title 					varchar(32) 		UNIQUE NOT NULL
  ,description 				varchar(512)
)
;

CREATE TABLE books_data.books (
  book_id	 				integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,title 					varchar(256) 		NOT NULL
  ,description 				varchar(1024)
  ,year_of_publish 			smallint 			NOT NULL 		CHECK (year_of_publish BETWEEN 0 AND EXTRACT(YEAR FROM CURRENT_DATE))
  ,publisher_id 			smallint 			NOT NULL 		REFERENCES books_data.publishers (publisher_id) 
  																			DEFERRABLE INITIALLY IMMEDIATE 
  ,language_id 				smallint 			NOT NULL		REFERENCES books_data.languages (language_id) 
  																			DEFERRABLE INITIALLY IMMEDIATE
  ,age_rating               age_rating_enum
  ,price 					money 				NOT NULL 		CHECK (price >= 0::money) DEFAULT 0::money
  ,text_url 				varchar(256)
  ,cover_url				varchar(256)		
  ,created_at 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
)
;

CREATE TABLE books_data.books_changeable (
  book_id					integer 			PRIMARY KEY 	REFERENCES books_data.books(book_id) 
  																			ON DELETE CASCADE 
																			DEFERRABLE INITIALLY IMMEDIATE
  ,rating 					numeric(3,2) 						CHECK (rating >= 0.00 AND rating <= 5.00) DEFAULT 0.00
  ,watched 					integer 			NOT NULL 		CHECK (watched >= 0) DEFAULT 0
)
;

CREATE TABLE books_data.author_book (
  author_id 				integer 			NOT NULL REFERENCES books_data.authors(author_id)
								  							ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,book_id 					integer 			NOT NULL REFERENCES books_data.books(book_id)
									  						ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,PRIMARY KEY(author_id, book_id)
)
;

CREATE TABLE books_data.book_genre (
  book_id 					integer				NOT NULL REFERENCES books_data.books(book_id)
							  								ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,genre_id 				smallint 			NOT NULL REFERENCES books_data.genres(genre_id)
							 								ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,PRIMARY KEY(book_id, genre_id)
)
;

-------------
-- clients --

CREATE TABLE clients.users (
  user_id					integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,login 					varchar(256) 		UNIQUE NOT NULL	CHECK(LENGTH(login) >= 6)
  ,password_hash 			varchar(512) 		NOT NULL
  ,nickname					varchar(512)		NOT NULL	
  ,organisation_id 			smallint			DEFAULT NULL 	
  ,created_at 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
)
;

CREATE TABLE clients.personal_data (
  user_id 					integer 			PRIMARY KEY     REFERENCES clients.users(user_id)
  ,email 					varchar(256) 		UNIQUE			CHECK (email ~ '^([\w]+[.-]{0,1}[\w]+)+@([a-zA-Z0-9]+([.-])*[a-zA-Z0-9]+)+\.+[a-zA-Z]{2,}$')
  ,phonenumber	 			varchar(20) 		UNIQUE			CHECK(phonenumber ~ '^\+\d{11,15}')
  ,surname					varchar(256)
  ,first_name				varchar(256)
  ,second_name				varchar(256)
  ,birthdate				date				NOT NULL		CHECK(birthdate BETWEEN '1900-01-01'::date AND CURRENT_DATE)
  ,payment					jsonb
  ,CONSTRAINT email_or_phone_required CHECK (email IS NOT NULL OR phonenumber IS NOT NULL)
)
;

CREATE TABLE clients.organisations (
  owner_id 					integer 			UNIQUE NOT NULL REFERENCES clients.users(user_id) 
  																		DEFERRABLE INITIALLY IMMEDIATE																	  
  ,organisation_id 			smallint 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,organisation_name 		varchar(64) 		NOT NULL UNIQUE
  ,created_at 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
)
;

ALTER TABLE clients.users 		ADD FOREIGN KEY (organisation_id) 
								REFERENCES clients.organisations (organisation_id) 
								DEFERRABLE INITIALLY IMMEDIATE
;

---------------------
-- subscribes_data --

CREATE TABLE subscribes_data.subscribe_types (
  "id" 						smallint 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,title 					varchar(64) 		NOT NULL
  ,"info"					varchar(512)
  ,price 					money 				NOT NULL 		CHECK(price >= 0::money) DEFAULT 0::money
  ,duration 				interval 			NOT NULL
  ,created_at				timestamp			NOT NULL		DEFAULT CURRENT_TIMESTAMP
)
;

CREATE TABLE subscribes_data.subscribe_book (
  subscribe_id 				smallint 			NOT NULL REFERENCES subscribes_data.subscribe_types("id")
							 								ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,book_id 					integer 			NOT NULL REFERENCES books_data.books(book_id)
							 								ON DELETE CASCADE
															DEFERRABLE INITIALLY IMMEDIATE
  ,PRIMARY KEY(subscribe_id, book_id)
)
;

-------------------
-- payments_data --

CREATE TABLE payments_data.cheques (
  cheque_id 				integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,user_id 					integer 			NOT NULL		REFERENCES clients.users(user_id)
    																	DEFERRABLE INITIALLY IMMEDIATE															
  ,total_cost 				money 				NOT NULL 		CHECK(total_cost >= 0::money)
  ,cheque_info 				varchar(128) 		NOT NULL
  ,cheque_date 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
)
;

CREATE TABLE payments_data.contracts (
  contract_id 				integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,subscribe_id				smallint 			NOT NULL		REFERENCES subscribes_data.subscribe_types("id")
  																		DEFERRABLE INITIALLY IMMEDIATE																	  
  ,organisation_id 			smallint 			NOT NULL		REFERENCES clients.organisations(organisation_id)
  																		DEFERRABLE INITIALLY IMMEDIATE																	  
  ,total_cost 				money	 			NOT NULL 		CHECK(total_cost >= 0::money)
  ,start_date				date				NOT NULL		DEFAULT CURRENT_DATE
  ,end_date					date 				NOT NULL 		CHECK(end_date > start_date)
  ,contract_info 			varchar(256) 		
  ,contract_date 			date 				NOT NULL 		DEFAULT CURRENT_DATE
  ,CONSTRAINT contract_date_logic CHECK (start_date >= contract_date AND contract_date <= CURRENT_DATE)
)
;

CREATE TABLE payments_data.cheque_book (
  cheque_id 				integer 			NOT NULL REFERENCES payments_data.cheques(cheque_id)
  															DEFERRABLE INITIALLY IMMEDIATE
  ,book_id 					integer 			NOT NULL REFERENCES books_data.books(book_id)
  															DEFERRABLE INITIALLY IMMEDIATE
  ,PRIMARY KEY(cheque_id, book_id)
)
;

CREATE TABLE payments_data.cheque_contract (
  cheque_id 				integer 			UNIQUE NULL REFERENCES payments_data.cheques(cheque_id)
  															DEFERRABLE INITIALLY IMMEDIATE
  ,contract_id 				integer 			UNIQUE NULL REFERENCES payments_data.contracts(contract_id)
  															DEFERRABLE INITIALLY IMMEDIATE
  ,PRIMARY KEY(cheque_id, contract_id)
)
;

-- books + users
CREATE TABLE books_data.user_book (
  user_id 					integer 			NOT NULL		REFERENCES clients.users(user_id)
			  							 								ON DELETE CASCADE
																		DEFERRABLE INITIALLY IMMEDIATE
  ,book_id 					integer 			NOT NULL		REFERENCES books_data.books(book_id)
			  							 								ON DELETE CASCADE
																		DEFERRABLE INITIALLY IMMEDIATE
  ,percentage 				numeric(5,2) 		NOT NULL 		CHECK(percentage >= 0.00 AND percentage <= 100.00) DEFAULT 0.00
  ,PRIMARY KEY(user_id, book_id)
)
;

CREATE TABLE books_data.reviews (
  review_id 				integer 			PRIMARY KEY		GENERATED ALWAYS AS IDENTITY
  ,user_id 					integer 			NOT NULL		REFERENCES clients.users(user_id)
    																	DEFERRABLE INITIALLY IMMEDIATE															
  ,book_id 					integer 			NOT NULL		REFERENCES books_data.books(book_id)
  																		DEFERRABLE INITIALLY IMMEDIATE																	  
  ,review 					varchar(4096)
  ,rating 					smallint	 		NOT NULL		CHECK (rating >= 0.00 AND rating <= 5.00)
  ,created_at 				timestamp 			NOT NULL 		DEFAULT CURRENT_TIMESTAMP
  ,UNIQUE(user_id,book_id)
)
;

								------------------
								-- INDEXES ZONE --
								------------------
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE 			INDEX ON    books_data.books 				    USING gin (title gin_trgm_ops);
CREATE 			INDEX ON 	books_data.books 				    (price);
CREATE 			INDEX ON 	books_data.books 				    (language_id);
CREATE 			INDEX ON 	books_data.books 				    (publisher_id);

CREATE 			INDEX ON 	books_data.authors				    USING gin (author_name gin_trgm_ops);
CREATE 			INDEX ON 	books_data.books_changeable		    (rating);
CREATE 			INDEX ON 	books_data.books_changeable		    (watched);

CREATE 		 	INDEX ON 	books_data.reviews 			        (rating);
CREATE 		 	INDEX ON 	books_data.reviews 			        (created_at);

CREATE  		INDEX ON 	clients.users				        (organisation_id);
CREATE  		INDEX ON 	clients.personal_data		        (user_id);
CREATE  		INDEX ON 	clients.personal_data		        USING gin(payment);

CREATE  		INDEX ON 	clients.organisations			    (owner_id);

CREATE  		INDEX ON 	payments_data.cheques				(user_id);
CREATE  		INDEX ON 	payments_data.cheques				(cheque_date);

CREATE  		INDEX ON 	payments_data.contracts 			(contract_date);
CREATE  		INDEX ON 	payments_data.contracts 			(end_date);
CREATE  		INDEX ON 	payments_data.contracts 			(organisation_id);
CREATE  		INDEX ON 	payments_data.contracts 			(subscribe_id);

CREATE 	 		INDEX ON 	subscribes_data.subscribe_types 	(title);
CREATE  		INDEX ON 	subscribes_data.subscribe_types 	(price);
CREATE  		INDEX ON 	subscribes_data.subscribe_types 	(duration);