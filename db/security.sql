CREATE ROLE game_tracker LOGIN PASSWORD '123isastrongPassword!';

REVOKE ALL ON DATABASE postgres FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT CONNECT ON DATABASE postgres TO game_tracker;
GRANT USAGE ON SCHEMA public TO game_tracker;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO game_tracker;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO game_tracker;

-- helper functions

CREATE OR REPLACE FUNCTION app_user_id() RETURNS integer LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.current_user_id', true), '')::integer $$;
 
CREATE OR REPLACE FUNCTION app_is_admin() RETURNS boolean LANGUAGE sql STABLE AS
$$ SELECT COALESCE(current_setting('app.is_admin', true) = 'true', false) $$;

-- games table

ALTER TABLE "games" ENABLE ROW LEVEL SECURITY;
CREATE POLICY games_read  ON "games" FOR SELECT USING (true);
CREATE POLICY games_admin ON "games" FOR ALL USING (app_is_admin());

-- user games table

ALTER TABLE "user_games" ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_games_read  ON "user_games" FOR SELECT USING (true);
CREATE POLICY user_games_owner ON "user_games" FOR ALL    USING (user_id = app_user_id());
CREATE POLICY user_games_admin ON "user_games" FOR ALL    USING (app_is_admin());

-- user profile table

ALTER TABLE "user_profiles" ENABLE ROW LEVEL SECURITY;
CREATE POLICY profiles_read  ON "user_profiles" FOR SELECT USING (true);
CREATE POLICY profiles_owner ON "user_profiles" FOR ALL    USING (user_id = app_user_id());
CREATE POLICY profiles_admin ON "user_profiles" FOR ALL    USING (app_is_admin());