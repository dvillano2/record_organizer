"""
Functions that takes path to a html file and returns
zip object of all for sale rows
"""
import re
from bs4 import BeautifulSoup


def total_data(price_html):
    """Gets total price and whether it is exact or not"""
    totals = [
        p_html.find("span", {"class": "converted_price"}).get_text().strip()
        for p_html in price_html
    ]

    totals = [total.split() for total in totals]
    est_exact = []

    for total in totals:
        if total[-1] != "total":
            est_exact.append(None)
        elif total[0] == "about":
            est_exact.append("Estimate")
        else:
            est_exact.append("Exact")

    for i, es_ex in enumerate(est_exact):
        if es_ex is None:
            totals[i] = None
        elif es_ex == "Estimate":
            totals[i] = totals[i][1]
        else:
            totals[i] = totals[i][0]

    total = [float(t.replace("$", "")) if t else None for t in totals]
    return total, est_exact


def lp_data(price_html):
    """Gets the listed price and the currency"""
    l_price = [
        p_html.find("span", {"class": "price"}).get_text().strip()
        for p_html in price_html
    ]
    currency = [re.sub(r"\d.*$", "", lp) for lp in l_price]
    for i, curr in enumerate(currency):
        if curr == "$":
            currency[i] = "USD"
        elif curr == "€":
            currency[i] = "EUR"
        elif curr == "CA$":
            currency[i] = "CAD"
        elif curr == "£":
            currency[i] = "GBP"
        elif curr == "¥":
            currency[i] = "JPY"
        elif curr == "A$":
            currency[i] = "AUD"

    l_price = [re.sub(r"^[^\d]*", "", lp).replace(",", "") for lp in l_price]
    return list(map(float, l_price)), currency


def shipping_data(price_html):
    """Gets shipping price"""
    ship = [p.find("span", {"class": "item_shipping"}) for p in price_html]

    def s_help(forest):
        """decomposes irrelevant spans"""
        for tree in forest.find_all("i"):
            tree.decompose()
        for tree in forest.find_all("button"):
            tree.decompose()
        return forest.get_text().strip()

    ship = [re.sub(r"^[^\d]*", "", s_help(sp)).replace(",", "") for sp in ship]
    return [float(s_p) if s_p else None for s_p in ship]


def media_data(cond_html):
    """Pulls the media conditions"""
    m_cond = map(lambda x: x.find_all("span")[2], cond_html)

    def mc_help(forest):
        """decomposes irrevant spans"""
        for tree in forest.find_all("span"):
            tree.decompose()
        return forest.get_text().strip()

    return [mc_help(m_c) for m_c in m_cond]


def ships_from_data(seller_html):
    """Pulls shipping countries"""
    s_loc = [s.find_all("li")[2] for s in seller_html]
    for s_l in s_loc:
        s_l.find("span").decompose()
    return [s_l.get_text().strip() if s_l else None for s_l in s_loc]


def forsaleprocess(path):
    with open(path, "r", encoding="utf8") as file:
        soup = BeautifulSoup(file, "html.parser")

        cond = soup.find_all("p", {"class": "item_condition"})
        nte = soup.find_all("p", {"class": "hide_mobile"})
        nte = [n for n in nte if n.find("span", {"class": "mplabel"}) is None]
        seller = soup.find_all("td", {"class": "seller_info"})
        price = soup.find_all("td", {"class": "item_price hide_mobile"})

        # total usd and exact/estimate
        total, est_exact = total_data(price)

        # list price and currency
        list_price, currency = lp_data(price)

        # shipping price
        shipping_price = shipping_data(price)

        # media condition
        media_cond = media_data(cond)

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
        nte = [n.get_text().strip() for n in nte]

        # SHIPS FROM
        ships_from = ships_from_data(seller)

        return zip(
            *[
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
                nte,
            ]
        )
