"""
Function that takes path to the html and returns an item row
"""
import json
from datetime import datetime
from bs4 import BeautifulSoup


def get_soup_info(bsoup):
    """Returns relevant subsoups"""
    sinfo = {}
    sinfo["url"] = bsoup.find("link", {"hreflang": "en"})["href"]
    sinfo["stats"] = bsoup.find("ul", {"class": "last"})
    sinfo["json"] = json.loads(
        bsoup.find(
            "script", {"type": "application/ld+json"}, {"id": "release_schema"}
        ).text
    )
    return sinfo


def get_sales_stats(stats_soup):
    """Gets the sales entries from the prepared stats soup"""
    l_sold = stats_soup.find("li", {"class": "last_sold"}).get_text().strip()
    if l_sold == "Never":
        l_sold = None
        low = None
        mid = None
        high = None
    else:
        l_sold = datetime.strptime(l_sold, "%d %b %y").date()
        mid_stats = stats_soup.find_all("li")[1:]
        low = float(mid_stats[0].get_text().strip()[1:])
        mid = float(mid_stats[1].get_text().strip()[1:])
        high = float(mid_stats[2].get_text().strip()[1:])

    return l_sold, low, mid, high


def itemprocess(path):
    """Returns release row for the corresponding html file"""
    with open(path, "r", encoding="utf-8") as file:
        subinfos = get_soup_info(BeautifulSoup(file, "html.parser"))

        url = subinfos["url"].strip()

        for span in subinfos["stats"].find_all("span"):
            span.decompose()

        last_sold, lowest, median, highest = get_sales_stats(subinfos["stats"])

        date_pub = subinfos["json"]["datePublished"]
        rel_name = subinfos["json"]["name"]
        label = subinfos["json"]["recordLabel"][0]["name"]

        # All artists involved, separated by semicolons
        artists = ""
        for artist in subinfos["json"]["releaseOf"]["byArtist"]:
            artists = artists + artist["name"] + "; "
        artists = artists[:-2]

        return (
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
