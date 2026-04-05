--alter table issue_history
--alter column field_changed drop not null; 

alter table issues
add constraint chk_issue_type
check (issue_type in ('bug', 'incident', 'request'));

alter table issues 
add constraint chk_priority
check (priority in ('low', 'medium', 'high', 'critical')); 

alter table issues
add constraint chk_status
check (status in ('open', 'in_progress', 'blocked', 'resolved')); 

-- why this is strong (tying back to CS 561 course)
-- we just implemented 
	-- Primary Keys --> entity identity 
	-- Foreign Keys --> referential integrity
	-- Atomic attributes (1NF) --> no multi-valued fields
	-- Controlled domains --> via CHECK constraints 
	-- Separation of concerns --> users vs issues vs history 