from process.itemprocess import itemprocess
from process.forsaleprocess import forsaleprocess
from itemupsert.itemupsert import itemupsert 
from forsaleupsert.forsaleupsert import forsaleupsert

wi_path = "data/textfiles/websiteinfo.txt"
db_path = "data/database/maindb.db"
row = itemprocess(wi_path)
rows = forsaleprocess(wi_path)
rel_id = itemupsert(row, db_path)
forsaleupsert(rows, db_path, rel_id)
