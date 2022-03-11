import requests
from bs4 import BeautifulSoup


def parse_urls():
    URL = "https://ddosmonitor.herokuapp.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    trs = soup.findAll('tr')

    list = []
    for tr in trs:
        if (tr.get('style') and tr["style"] in {"background-color: lightgreen", "background-color: lightblue"}):
            data = tr.contents[7].text
            if data.startswith('http'):
                list.append(data)

    return list


# with open('urls.txt', "w") as urls_file:
#     for url in parse_urls():
#         urls_file.write(f"{url}\n")
