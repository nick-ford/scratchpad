CREATE TABLE guests (
  id integer,
  partyName text,
  guestOrder integer,
  firstName text collate nocase,
  lastName text collate nocase
);

CREATE TABLE responses (
  id integer primary key,
  firstName text,
  lastName text,
  attending boolean default 't',
  mealchoice integer,
  notes text,
  email text,
  submitted datetime
);

CREATE TRIGGER insert_response_created after insert on responses
begin
  update responses set submitted = datetime('now')
  where rowid = new.rowid;
end;

.quit
