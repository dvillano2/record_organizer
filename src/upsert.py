""" Pulls all the upserting together """
from process.itemprocess import itemprocess
from process.forsaleprocess import forsaleprocess
from itemupsert.itemupsert import itemupsert
from forsaleupsert.forsaleupsert import forsaleupsert

WI_PATH = "data/textfiles/websiteinfo.txt"
DB_PATH = "data/database/maindb.db"
row = itemprocess(WI_PATH)
rows = forsaleprocess(WI_PATH)
rel_id = itemupsert(row, DB_PATH)
forsaleupsert(rows, DB_PATH, rel_id)
