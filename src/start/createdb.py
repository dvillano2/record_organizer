""" Function that creates the database """
import sqlite3


def createdb(path):
    """Creates the database, takes one arg: path to the db"""
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS releases(
        id INTEGER PRIMARY KEY,
        release_name VARCHAR(100),
        artist VARCHAR(100),
        record_label VARCHAR(100),
        year_released INTEGER,
        median_price DIGIT(6, 2),
        highest_price DIGIT(6, 2),
        lowest_price DIGIT(6, 2),
        last_sold TIMESTAMP,
        url VARCHAR(300),
        date_added TIMESTAMP,
        last_updated TIMESTAMP,
        UNIQUE(release_name, artist, record_label, year_released)
        )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS for_sale(
        id INTEGER PRIMARY KEY,
        release_id INTEGER,
        total_USD DIGIT(6, 2),
        estimate TEXT CHECK( estimate IN ('Exact', 'Estimate') ),
        media_condition VARCHAR(60),
        sleeve_condition VARCHAR(60),
        price DIGIT(6, 2),
        shipping_price DIGIT(6, 2),
        ships_from VARCHAR(30),
        currency CHAR(3),
        seller VARCHAR(60),
        total_ratings INTEGER,
        average_rating DIGIT(6,2),
        Notes VARCHAR(300),
        date_identified TIMESTAMP,
        date_removed TIMESTAMP,
        purchased INTEGER DEFAULT 0,
        FOREIGN KEY(release_id) REFERENCES releases(id),
        UNIQUE (media_condition, sleeve_condition, price, seller, date_removed)
        )"""
    )

    con.commit()
    con.close()
