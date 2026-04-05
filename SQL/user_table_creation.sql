-- ==============================================
-- # User table creation
-- ==============================================


create table users (
	user_id serial primary key,
	full_name varchar(100) not null,
	email varchar(100) unique not null,
	role varchar(20) not null,
	created_at timestamp default current_timestamp
); 

-- SERIAL: auto-incrementing primary key
-- UNIQUE(email): enforces no duplicate users 
-- NOT NULL: required fields 