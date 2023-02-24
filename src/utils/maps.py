import requests
from bs4 import BeautifulSoup
import json


def get_ll_from_yandex_url(url):
    cookies = {
        'maps_los': '1',
        'yandexuid': '4484608141665841531',
        'yuidss': '4484608141665841531',
        'ymex': '1981201534.yrts.1665841534#1981201533.yrtsi.1665841533',
        'gdpr': '0',
        '_ym_uid': '1665841534346238104',
        'font_loaded': 'YSv1',
        '_ym_d': '1670143851',
        'skid': '9186831611672583850',
        'i': 'E+YLZ0hylndM5YWC/QzRkh0l6rlnhDtEV3MCieandmGUuo2DggT/8FMZcCbgfTpZ2LntLGmeyBMqibzs/B6OepQf/eE=',
        'yashr': '6989586641674196974',
        'L': 'X1ZUQElYYmFxBV1UWXF4X1ZfDFVoBE9HI1gLBBMwSQ==.1676836640.15258.394068.334915a9383802dada6d769cc910d86c',
        'yandex_login': 'laggayy',
        'ys': 'udn.cDpsYWdnYXl5#c_chck.4269790893',
        'is_gdpr': '0',
        'is_gdpr_b': 'CIG7UxC+qAEoAg==',
        'Session_id': '3:1677239271.5.0.1676836457805:tlRuwg:21.1.2:1|1737430517.182.2.2:182.3:1676836639|3:10266049.485300.mVj7QgpljLQPFNqTE4H3LBQJ2go',
        'sessionid2': '3:1677239271.5.0.1676836457805:tlRuwg:21.1.2:1|1737430517.182.2.2:182.3:1676836639|3:10266049.485300.fakesign0000000000000000000',
        '_yasc': 'kw7RZpa4kbO1qH5GK+l7qNtBxUvhpvz5+W8n1ro3ywc8+BgumxS0JrB1OelQoBA8',
        'spravka': 'dD0xNjc3MjQ3ODAzO2k9MTg4LjEzMC4xNTUuMTY1O0Q9MERGMUU1RDFBMzE2NjA5MjA5MzU1Q0UwQTNGRkNFMkQzNUQxQkQ3OEE3NTgxQkE0RkU1NzAyMTk2NURENDk4OUY4MjA0RTE1MkMxMjNFO3U9MTY3NzI0NzgwMzg5NDUyODMyODtoPTkxNzBiMmMyZmIxZTY0OThlNjMzNzRhYmFiM2IzZmVm',
        'yp': '1702386125.pgp.2_27847473#1988880220.pcs.0#1987944979.multib.1#1992196639.udn.cDorNzk4NjkyNDk4NzQ%3D#1677420635.gpauto.55_753932:48_742985:14:0:1677247825',
    }

    headers = {
        'authority': 'yandex.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8,ru;q=0.7',
        # 'cookie': 'maps_los=1; yandexuid=4484608141665841531; yuidss=4484608141665841531; ymex=1981201534.yrts.1665841534#1981201533.yrtsi.1665841533; gdpr=0; _ym_uid=1665841534346238104; font_loaded=YSv1; _ym_d=1670143851; skid=9186831611672583850; i=E+YLZ0hylndM5YWC/QzRkh0l6rlnhDtEV3MCieandmGUuo2DggT/8FMZcCbgfTpZ2LntLGmeyBMqibzs/B6OepQf/eE=; yashr=6989586641674196974; L=X1ZUQElYYmFxBV1UWXF4X1ZfDFVoBE9HI1gLBBMwSQ==.1676836640.15258.394068.334915a9383802dada6d769cc910d86c; yandex_login=laggayy; ys=udn.cDpsYWdnYXl5#c_chck.4269790893; is_gdpr=0; is_gdpr_b=CIG7UxC+qAEoAg==; Session_id=3:1677239271.5.0.1676836457805:tlRuwg:21.1.2:1|1737430517.182.2.2:182.3:1676836639|3:10266049.485300.mVj7QgpljLQPFNqTE4H3LBQJ2go; sessionid2=3:1677239271.5.0.1676836457805:tlRuwg:21.1.2:1|1737430517.182.2.2:182.3:1676836639|3:10266049.485300.fakesign0000000000000000000; _yasc=kw7RZpa4kbO1qH5GK+l7qNtBxUvhpvz5+W8n1ro3ywc8+BgumxS0JrB1OelQoBA8; spravka=dD0xNjc3MjQ3ODAzO2k9MTg4LjEzMC4xNTUuMTY1O0Q9MERGMUU1RDFBMzE2NjA5MjA5MzU1Q0UwQTNGRkNFMkQzNUQxQkQ3OEE3NTgxQkE0RkU1NzAyMTk2NURENDk4OUY4MjA0RTE1MkMxMjNFO3U9MTY3NzI0NzgwMzg5NDUyODMyODtoPTkxNzBiMmMyZmIxZTY0OThlNjMzNzRhYmFiM2IzZmVm; yp=1702386125.pgp.2_27847473#1988880220.pcs.0#1987944979.multib.1#1992196639.udn.cDorNzk4NjkyNDk4NzQ%3D#1677420635.gpauto.55_753932:48_742985:14:0:1677247825',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1',
        'ect': '4g',
        'rtt': '50',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-arch': '"arm"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"108.0.5359.124"',
        'sec-ch-ua-full-version-list': '"Not?A_Brand";v="8.0.0.0", "Chromium";v="108.0.5359.124", "Google Chrome";v="108.0.5359.124"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"13.1.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'viewport-width': '1157',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    bs = BeautifulSoup(response.content, features="html.parser")
    test = bs.find("script", {"class": "state-view"}).next
    js = json.loads(test)
    return js['config']['query']['ll'].split(',')
