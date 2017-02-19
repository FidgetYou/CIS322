/*
This is the table for usernames and passwords.
I decided to use a primary key because I like it.
I also like the idea of a single numbered column counting everything.
If it was just built with the username as the primary key it wouldn't feel ordered to me.
I chose the password length to be 16 because the design spec said that it wouldn't be longer than 16.
Unless I went with a hash to store passwords... Which I didn't. (Security isn't really my thing right now.)
Etc. To be added later.
*/
CREATE TABLE user_name(
	user_pk		serial primary key,
	username	varchar(16),
	password	varchar(16),
	jobtitle	varchar(25)
);

