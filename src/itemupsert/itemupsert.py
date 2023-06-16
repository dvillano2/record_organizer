from datetime import datetime
import sqlite3

"""
Funtion that takes the row of the item to be added and adds or updates it 
Returns the id of the release, whether or not its already in the database
"""
def itemupsert(row, path_to_db):

	row = list(row)
	row += [datetime.now().date()] * 2

	### Open SQLite connection and put it in the database or update the appropriate row
	###
	con = sqlite3.connect(path_to_db)
	cur = con.cursor()

	placeholders = ', '.join('?' * 11)
	cols = 'release_name, artist, record_label, year_released, median_price, highest_price, lowest_price, last_sold, url, date_added, last_updated'
	uniq_ind = 'release_name, artist, record_label, year_released'
	med_up = 'median_price = excluded.median_price'
	high_up = 'highest_price = excluded.highest_price'
	low_up = 'lowest_price = excluded.lowest_price'
	lsold_up  = 'last_sold = excluded.last_sold'
	lup_up = 'last_updated = excluded.last_updated'
	sql ='INSERT INTO releases({}) VALUES ({}) ON CONFLICT({}) DO UPDATE SET {}, {}, {}, {}, {} RETURNING id'.format(cols, placeholders, uniq_ind, med_up, high_up, low_up, lsold_up, lup_up)

	cur.execute(sql, row)
	release_id = cur.fetchone() 
	con.commit()

	cur.close()
	con.close()

	return release_id[0]
