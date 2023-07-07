CREATE TABLE "criptos" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"fiat"	TEXT NOT NULL,
    "fiat_inverted" REAL NOT NULL,
	"cripto"	REAL NOT NULL,
    "cripto_conversed"  REAL NOT NULL,
	"rate"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);