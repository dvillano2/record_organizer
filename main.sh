#!/bin/bash

### FILEPATHS
readonly DB_PATH="data/database/maindb.db"
readonly WINFO_PATH="data/textfiles/websiteinfo.txt"

### Create the database and pull relevant info
if [[ "$1" = 'start' ]]; then
	mkdir -p data/database
	mkdir -p data/textfiles
	touch $WINFO_PATH
	sqlite3 $DB_PATH "VACUUM;"
	python3 -c'from src.start.createdb import createdb; createdb("data/database/maindb.db"); exit()'
	exit
elif [[ "$1" = 'add' ]]; then
	curl -s "$2" > $WINFO_PATH
elif [[ "$1" = 'update' ]]; then
	url=$(python3 -c'from src.findurl.findurl import findurl; print(findurl('$2', "data/database/maindb.db"))')
	if [[ "$url" = 'No such release' ]]; then
		exit
	fi
	curl -s "$url" > $WINFO_PATH
fi

### Excute the additons/upserts
python3 src/upsert.py
