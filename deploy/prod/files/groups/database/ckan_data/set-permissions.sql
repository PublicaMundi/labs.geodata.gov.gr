/*
This script sets-up the permissions for the the CKAN datastore.
Must be invoked as database superuser (postgres).
*/

-- name of the main CKAN database
\set maindb "ckan"
-- the name of the datastore database
\set datastoredb "ckan_data"
-- username of the ckan postgres user
\set ckanuser "ckaner"
-- username of the datastore user that can write
\set wuser "ckan_datastorer"
-- username of the datastore user who has only read permissions
\set rouser "ckan_datareader"

-- revoke permissions for the read-only user
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE USAGE ON SCHEMA public FROM PUBLIC;

GRANT CREATE ON SCHEMA public TO :ckanuser;
GRANT USAGE ON SCHEMA public TO :ckanuser;

GRANT CREATE ON SCHEMA public TO :wuser;
GRANT USAGE ON SCHEMA public TO :wuser;

-- take connect permissions from main CKAN db
REVOKE CONNECT ON DATABASE :maindb FROM :rouser;

-- grant select permissions for read-only user
GRANT CONNECT ON DATABASE :datastoredb TO :rouser;
GRANT USAGE ON SCHEMA public TO :rouser;

-- grant access to current tables and views to read-only user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO :rouser;
