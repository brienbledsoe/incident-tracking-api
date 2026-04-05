-- ==============================================
-- # Issue History Table Creation
-- ==============================================

create table issue_history (
	history_id serial primary key, 
	issue_id integer not null, 
	changed_by integer not null,
	action_type varchar(50) not null,
	field_changed varchar(50) not null, 
	old_value text,
	new_value text,
	changed_at timestamp default current_timestamp,

	constraint fk_issue
		foreign key (issue_id)
		references issues(issue_id),

	constraint fk_changed_by
		foreign key (changed_by)
		references users(user_id)

); 










