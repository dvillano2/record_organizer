""" Function and helper that
takes the for sale rows and inserts or updates them
"""
from datetime import datetime
import sqlite3


def sql_upsert():
    """returns complictaed sql upsert query"""
    cols = (
        "total_USD, "
        "estimate, "
        "media_condition, "
        "sleeve_condition, "
        "price, shipping_price, "
        "ships_from, "
        "currency, "
        "seller, "
        "total_ratings, "
        "average_rating, "
        "Notes, "
        "date_removed, "
        "release_id"
    )
    placeholders = ", ".join("?" * 14)
    uniq_ind = "media_condition, sleeve_condition, price, seller, date_removed"
    tot_up = "total_USD=excluded.total_USD"
    totr_up = "total_ratings=excluded.total_ratings"
    avr_up = "average_rating=excluded.average_rating"
    not_up = "Notes=excluded.Notes"
    datr_up = "date_removed = NULL"
    return (
        f"INSERT INTO for_sale({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT({uniq_ind}) DO UPDATE SET "
        f"{tot_up}, {totr_up}, {avr_up}, {not_up}, {datr_up}"
    )


def forsaleupsert(rows, path_to_db, rel_id):
    """takes list of for sale rows and
    inserts or updates the corresponding rows in the db
    """
    rows = [list(r) + [datetime.now().date(), rel_id] for r in rows]
    rows = [tuple(r) for r in rows]

    # Open SQLite connection and put it in the database
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    # Set date removed for all appropriate for sale items to today
    # will be changed back to NULL if there is a match
    sql_date_removed = (
        "UPDATE for_sale SET date_removed = ? "
        "WHERE release_id = ? AND date_removed IS NULL"
    )
    cur.execute(sql_date_removed, (datetime.now().date(), rel_id))

    # Insert new for sales into the db if they're not already there
    # otherwise update toatal price etc and flip date_removed back to NULL
    cur.executemany(sql_upsert(), rows)

    # Flip date_removed and date_identifed for new entries
    sql_flip_dates = (
        "UPDATE for_sale SET date_identified "
        "= date_removed, date_removed = NULL WHERE date_identified IS NULL"
    )
    cur.execute(sql_flip_dates)

    con.commit()

    cur.close()
    con.close()
