""" Pulls all the upserting together """
from .process.itemprocess import itemprocess
from .process.forsaleprocess import forsaleprocess
from .itemupsert.itemupsert import itemupsert
from .forsaleupsert.forsaleupsert import forsaleupsert

WI_PATH = "data/textfiles/websiteinfo.txt"
DB_PATH = "data/database/maindb.db"


def upsert(wi_path, db_path):
    """upserts the db"""
    row = itemprocess(wi_path)
    rows = forsaleprocess(wi_path)
    rel_id = itemupsert(row, db_path)
    forsaleupsert(rows, db_path, rel_id)
