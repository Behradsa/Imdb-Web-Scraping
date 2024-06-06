import requests
from lxml import etree
import csv


def get_summery(link):
    link = "https://m.imdb.com/" + link.get("href")
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        tree = etree.HTML(html_content)
        sum = tree.xpath('//span[@class="sc-7193fc79-2 kpMXpM"]')
        summery = sum[0].text.strip()
        return summery
    else:
        print("Failed to fetch the webpage.")


url = "https://www.imdb.com/chart/top/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
scraped_summeries = []

my_dict = []
if response.status_code == 200:

    html_content = response.text
    tree = etree.HTML(html_content)
    # get movie-page links\
    links = tree.xpath('//a[@class="ipc-title-link-wrapper"]')
    h3_links = tree.xpath('//a[@class="ipc-title-link-wrapper"]/h3')

    for link in h3_links:

        if link.text[0].isdigit():
            rank = link.text.split(".", 1)[0]
            name = link.text.split(".", 1)[1].strip()

            my_dict.append({"rank": rank, "name": name})

    count = 0
    for link in links:
        if "title" in link.get("href"):
            my_dict[count]["summery"] = get_summery(link)
            print(count)
        count += 1

    fields = ["rank", "name", "summery"]

    filename = "data.csv"

    with open(filename, "w") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(my_dict)

else:
    print("Failed to fetch the webpage.")
