import time
import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib


def find_values(query):
    query = urllib.parse.quote_plus(query)  # Format into URL encoding
    number_result = 10
    ua = UserAgent()
    proxies = {
        'http': 'http://' + 'username' + ':' + 'password' + 'proxy_address',
        'https': 'http://' + 'username' + ':' + 'password' + 'proxy_address'
    }

    headers = {"Accept-Language": "en-US,en;q=0.5", 'Accept-Encoding': 'gzip, deflate'}
    google_url = "https://www.google.com/search?q=" + query + "&lr=lang_en&num=" + str(number_result)

    response = requests.get(google_url, {'User-Agent': ua.chrome}, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div')

    links = []
    titles = []
    descriptions = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class': 's3v9rd'}).get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '':
                descriptions.append(description)
                time.sleep(0.5)
        # Next loop if one element is not present
        except:
            continue

    return descriptions


def fetch_data():

    sw_list = pd.read_excel('swlist.xlsx')
    manu_list = sw_list['Manufacturer'].tolist()

    des = []
    u_des = []
    for manftr in manu_list:
        print("current -", manftr)
        descriptions = find_values(manftr)
        print(len(descriptions))
        if descriptions:
            des.append(descriptions[0])

            help_desc = []
            for desc in descriptions:
                if 'tool' or 'software' or 'hardware' or 'function' or 'GmbH' \
                        or 'install' or 'installation' or 'game' or 'tutorial' \
                        or 'work' or 'wokring' or 'device' or 'electric' \
                        or 'electronic' or 'technology' or 'tools' or 'micro' \
                        or 'program' in desc.lower():
                    help_desc.append(desc)

            help_desc = list(set(help_desc))
            if help_desc:
                u_des.append('.\n\n'.join(help_desc[0:5]))
            else:
                u_des.append('None')
        else:
            des.append('None')
            u_des.append('None')

    sw_list['Description'] = des
    sw_list['Useful Description'] = u_des
    sw_list.to_excel('result6.xlsx', index=False)


if __name__ == "__main__":
    fetch_data()

