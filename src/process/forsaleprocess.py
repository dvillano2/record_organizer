"""
Funciton that takes path to a html file and returns
zip object of all for sale rows
"""
import re
from bs4 import BeautifulSoup

def forsaleprocess(path):
    with open(path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

        cond = soup.find_all("p", {"class": "item_condition"})
        note = soup.find_all("p", {"class": "hide_mobile"})
        note = [n for n in note if n.find("span") is None]
        seller = soup.find_all("td", {"class": "seller_info"})
        price = soup.find_all("td", {"class": "item_price hide_mobile"})

        # TOTAL USD AND EXACT/ESTIMATE
        total = [
            p.find("span", {"class": "converted_price"}).get_text().strip()
            for p in price
        ]
        total = [t.split() for t in total]
        est_exact = []
        for t in total:
            if t[-1] != "total":
                est_exact.append(None)
            elif t[0] == "about":
                est_exact.append("Estimate")
            else:
                est_exact.append("Exact")

        for i, e in enumerate(est_exact):
            if e is None:
                total[i] = None
            elif e == "Estimate":
                total[i] = total[i][1]
            else:
                total[i] = total[i][0]
        total = [float(t.replace("$", "")) if t is not None else None for t in total]

        # LIST PRICE AND CURRENCY
        list_price = [
            p.find("span", {"class": "price"}).get_text().strip() for p in price
        ]
        currency = [re.sub("\d.*$", "", lp) for lp in list_price]
        for i, c in enumerate(currency):
            if c == "$":
                currency[i] = "USD"
            elif c == "€":
                currency[i] = "EUR"
            elif c == "CA$":
                currency[i] = "CAD"
            elif c == "£":
                currency[i] = "GBP"
            elif c == "¥":
                currency[i] = "JPY"
            elif c == "A$":
                currency[i] = "AUD"
        list_price = [re.sub("^[^\d]*", "", lp) for lp in list_price]
        list_price = [lp.replace(",", "") for lp in list_price]
        list_price = [float(lp) for lp in list_price]

        # SHIPPING PRICE
        shipping_price = [p.find("span", {"class": "item_shipping"}) for p in price]
        for sp in shipping_price:
            for t in sp.find_all("i"):
                t.decompose()
            for t in sp.find_all("button"):
                t.decompose()
        shipping_price = [sp.get_text().strip() for sp in shipping_price]
        shipping_price = [re.sub("^[^\d]*", "", sp) for sp in shipping_price]
        shipping_price = [sp.replace(",", "") for sp in shipping_price]
        shipping_price = [float(sp) if sp != "" else None for sp in shipping_price]

        # MEDIA CONDITION
        media_cond = map(lambda x: x.find_all("span"), cond)

        def med_cond_help(m):
            for s in m[2].find_all("span"):
                s.decompose()
            return m[2].get_text().strip()

        media_cond = list(map(med_cond_help, media_cond))

        # SLEEVE CONDITION
        sleeve_cond = map(
            lambda x: x.find("span", {"class": "item_sleeve_condition"}), cond
        )
        sleeve_cond = map(
            lambda x: x.get_text() if x else "No sleeve listed", sleeve_cond
        )
        sleeve_cond = list(sleeve_cond)

        # SELLER USERNAME AND NUMBER OF RATINGS
        name_rate = [s.find_all("a") for s in seller]
        seller_name = [nr[0].get_text().strip() for nr in name_rate]
        rate_count = [
            nr[1].get_text().strip() if len(nr) > 1 else None for nr in name_rate
        ]
        rate_count = [
            int("".join(filter(str.isdigit, rc))) if rc else None for rc in rate_count
        ]

        # AVERAGE RATING
        ave_rate = [s.find_all("strong") for s in seller]
        ave_rate = [
            ar[1].get_text().strip() if len(ar) > 1 else None for ar in ave_rate
        ]
        ave_rate = [float(ar.replace("%", "")) if ar else None for ar in ave_rate]

        # COMMENTS FROM SELLER
        note = [n.get_text().strip() for n in note]

        # SHIPS FROM
        ships_from = [s.find_all("li")[2] for s in seller]
        for sf in ships_from:
            sf.find("span").decompose()
        ships_from = [sf.get_text().strip() for sf in ships_from]

        biglist = [
            total,
            est_exact,
            media_cond,
            sleeve_cond,
            list_price,
            shipping_price,
            ships_from,
            currency,
            seller_name,
            rate_count,
            ave_rate,
            note,
        ]
        biglist = zip(*biglist)
        return biglist
