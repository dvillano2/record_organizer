""" Function that takes the id of a relase and returns its URL """
import sqlite3


def findurl(rel_id, path_to_db):
    """Take id, path, returns url"""
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    sql = "SELECT url FROM releases WHERE id = ?"
    cur.execute(sql, (rel_id,))

    url = [r[0] for r in cur.fetchall()]
    # print (url)
    if len(url) == 0:
        url = "No such release"
    else:
        url = url[0]

    cur.close()
    con.close()

    return url
