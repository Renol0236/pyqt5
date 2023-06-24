CREATE TABLE calc_history(
id INTEGER PRIMARY KEY,
result INTEGER NOT NULL,
line INTEGER NOT NULL,
tm VARCHAR NOT NULL
);
CREATE TABLE pass_history(
    id INTEGER PRIMARY KEY,
    pass VARCHAR NOT NULL,
    tm VARCHAR NOT NULL
);
CREATE TABLE currency_history(
    id INTEGER PRIMARY KEY,
    result INTEGER NOT NULL,
    "from" VARCHAR NOT NULL,
    "to" VARCHAR NOT NULL,
    tm INTEGER NOT NULL
);
CREATE TABLE notify_history(
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NUll,
    text VARCHAR NULL,
    expired INTEGER NOT NULL,
    tm INTEGER NOT NULL
);