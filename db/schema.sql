CREATE TABLE IF NOT EXISTS "users" (
	"user_id" SERIAL NOT NULL,
	"email" VARCHAR(120) NOT NULL,
	"password_hash" VARCHAR(255) NOT NULL,
	"is_admin" BOOLEAN NOT NULL DEFAULT FALSE,
	"created_at" DATE NOT NULL,
	PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "user_profiles" (
	"profile_id" SERIAL NOT NULL,
	"user_id" INTEGER NOT NULL,
	"username" VARCHAR(255) NOT NULL,
	"bio" TEXT,
	"avatar_url" VARCHAR(255),
	PRIMARY KEY("profile_id")
);

CREATE TABLE IF NOT EXISTS "games" (
	"game_id" SERIAL NOT NULL,
	"title" VARCHAR(150) NOT NULL,
	"description" TEXT,
	"release_year" INTEGER,
	"genre" VARCHAR(255),
	"cover_image_url" VARCHAR(255),
	PRIMARY KEY("game_id")
);

CREATE TABLE IF NOT EXISTS "user_games" (
	"id" SERIAL NOT NULL,
	"user_id" INTEGER NOT NULL,
	"game_id" INTEGER NOT NULL,
	"review" TEXT,
	"rating" INTEGER,
	PRIMARY KEY("id")
);

ALTER TABLE "user_profiles"
ADD FOREIGN KEY("user_id") REFERENCES "users"("user_id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "user_games"
ADD FOREIGN KEY("user_id") REFERENCES "users"("user_id")
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "user_games"
ADD FOREIGN KEY("game_id") REFERENCES "games"("game_id")
ON UPDATE NO ACTION ON DELETE CASCADE;