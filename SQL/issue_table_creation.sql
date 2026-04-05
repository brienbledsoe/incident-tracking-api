-- ==============================================
-- # Issue Table Creation
-- ==============================================

create table issues (
	issue_id serial primary key,
	title varchar(200) not null,
	description text,
	issue_type varchar(20) not null,
	priority varchar(20) not null, 
	status varchar(20) not null,
	created_by integer not null,
	assigned_to integer, 
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp,

	constraint fk_created_by
		foreign key (created_by)
		references users(user_id),

	constraint fk_assigned_to
		foreign key (assigned_to)
		references users(user_id)
); 

-- assigned_to can contain null values --> supports unassigned issues
-- Two foreign keys referencing users (very common patter)
-- TEXT used for description --> flexible length