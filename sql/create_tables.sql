/*
This is the table for usernames and passwords.
I decided to use a primary key because I like it.
I also like the idea of a single numbered column counting everything.
If it was just built with the username as the primary key it wouldn't feel ordered to me.
I chose the password length to be 16 because the design spec said that it wouldn't be longer than 16.
Unless I went with a hash to store passwords... Which I didn't. (Security isn't really my thing right now.)

I didn't want to have to add a table just for job titles... But if there is only going to be two, I might as well.
This way I can also make a drop down menu of job titles. You know, if I get around to it.
Apparently Job titles don't get their own creation page. So I'm just inputting the two we have here.
*/
CREATE TABLE role(
	role_pk		serial primary key,
	role		varchar(25)
);

INSERT INTO role (role) VALUES ('Logistics Officer');
INSERT INTO role (role) VALUES ('Facilities Officer');


CREATE TABLE user_name(
	user_pk		serial primary key,
	username	varchar(16),
	password	varchar(16),
	role_fk		integer REFERENCES role (role_pk) not null
);

/* 
COMMENTS! The reasons for the use of a primary numbered pk holds from previous entries.
*/
CREATE TABLE asset(
	asset_pk	serial primary key,
	asset_tag	varchar(16),
	asset_info	varchar(100)
);

/*
You wish there was info here. Comments aren't graded!       Woo..?
*/
CREATE TABLE facility(
	facility_pk	serial primary key,
	facility_name	varchar(32),
	facility_code	varchar(8),
	facility_info	varchar(150)
);	

/*
Where did I set my assets?

Based heavily on suggestions by the instructor. There is a column for the asset and facility's foriegn keys.
With a column for arrival and departure that will grow as the asset is moved and gains arrival ans departures.
I also added a column for whether the asset was in transit or not and whether or not it had been disposed of.
I'm not ye sure how well these will all work. But it looks workable so far. If disposed is TRUE you don't have
to look for another arrival time, but if in_transit is TRUE, then you do.
*/
CREATE TABLE asset_at(
	asset_fk	integer REFERENCES asset (asset_pk) not null,
	facility_fk	integer REFERENCES facility (facility_pk) not null,
	arrive		timestamp default null,
	depart		timestamp default null,
	in_transit	boolean default false,
	disposed	boolean default false
);

/*
Assignment 8 additions. The jokes aren't really any funnier the second time around. Sorry.

Tried to fit all of the needed request things in here. I think I got them all. But this seems to be rather complicated to track.
*/

CREATE TABLE requests(
	request_pk	serial primary key,
	asset_fk	integer REFERENCES asset (asset_tag) not null,
	requester	integer REFERENCES user_name (username) not null,
	approver	integer REFERENCES user_name (username) default null,
	source_fac	integer REFERENCES facility (facility_code) not null,
	destination_fac	integer REFERENCES facility (facility_code) not null,
	request_time	timestamp default null,
	approve_time	timestamp default null,
	approved	boolean default false,
	rejected	boolean default false,
	comments	varchar(300)
);















