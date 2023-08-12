from bs4 import BeautifulSoup
from datetime import datetime
import re
import json

"""
Function that takes path to the html and returns an item row 
"""


def itemprocess(path):
    with open(path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

        # LAST SOLD, LOWEST, MEDIAN, HIGHEST ALL HERE
        stats = soup.find("ul", {"class": "last"})

        for s in stats.find_all("span"):
            s.decompose()

        last_sold = stats.find("li", {"class": "last_sold"}).get_text().strip()
        if last_sold == "Never":
            last_sold = None
            lowest = None
            median = None
            highest = None
        else:
            last_sold = datetime.strptime(last_sold, "%d %b %y").date()
            mid_stats = stats.find_all("li")[1:]
            lowest = float(mid_stats[0].get_text().strip()[1:])
            median = float(mid_stats[1].get_text().strip()[1:])
            highest = float(mid_stats[2].get_text().strip()[1:])

        # URL
        url = soup.find("link", {"hreflang": "en"})["href"].strip()

        # All other info in json
        site_json = json.loads(
            soup.find(
                "script", {"type": "application/ld+json"}, {"id": "release_schema"}
            ).text
        )
        date_pub = site_json["datePublished"]
        rel_name = site_json["name"]

        # Picks the first record label listed in the schema
        label = site_json["recordLabel"][0]["name"]

        # All artists involved, separated by semicolons
        artists = ""
        for artist in site_json["releaseOf"]["byArtist"]:
            artists = artists + artist["name"] + "; "
        artists = artists[:-2]

        row = (
            rel_name,
            artists,
            label,
            date_pub,
            median,
            highest,
            lowest,
            last_sold,
            url,
        )
        return row
