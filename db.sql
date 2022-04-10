CREATE TABLE "users"(
    "id_AI" INTEGER,
    "full_name" TEXT,
    "password" TEXT,
    "real_id" TEXT UNIQUE,
    PRIMARY KEY ("id_AI" AUTOINCREMENT)
);

CREATE TABLE "Tickets"  (
    "ticket_id" INTEGER,
    "user_id" INTEGER,
    "flight_id" INTEGER,
    PRIMARY KEY ("ticket_id"),
    FOREIGN KEY ("user_id") REFERENCES users(id_AI),
    FOREIGN KEY ("flight_id") REFERENCES Flights(flights_id)
);

CREATE TABLE "Flights"  (
    "flights_id" INTEGER,
	"timestamp" TEXT,
	"remaining_seats" INTEGER,
	"origin_country_id" INTEGER,
	"dest_country_id" INTEGER,
	PRIMARY KEY ("flights_id"),
	FOREIGN KEY ("origin_country_id") REFERENCES Countries(code_AI),
	FOREIGN KEY ("dest_country_id") REFERENCES Countries(code_AI)
);

CREATE TABLE "Counties"  (
    "code_AI" INTEGER,
	"name" TEXT,
	PRIMARY KEY ("code_AI")
);
