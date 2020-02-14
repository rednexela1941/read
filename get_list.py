import requests as req
import re

from lxml import html, etree


URL = 'https://thegreatestbooks.org/'



def flatten(data):
    out = []
    for k in data:
        for j in k:
            out.append(j)
    return out

def scrape():
    books = []
    for k in range(1,21):
        link = URL + f"?page={k}"
        books.append(parse(link))
    return flatten(books)

def string_html(element):
    el = etree.tostring(element, pretty_print=True)
    return el
# https://thegreatestbooks.org/?page=4


def parse(url):
    page = req.get(url)
    tree = html.fromstring(page.content)
    books = []
    containers = tree.find_class("item pb-3 pt-3 border-bottom")
    for k in containers:
        # print(etree.tostring(k, pretty_print=True))
        element = k.find_class('col')[0].cssselect('h4')[0]
        try:
            amazon = k.find_class('pb-3')[0].find_class('pull-left mr-3')[0].cssselect('a')
            amazon_link = amazon[1].get("href")
            length = get_length(amazon_link)
        except:
            length = 0
        info = element.text_content()
        split = info.split('.')
        number = int(split[0])
        info = element.cssselect('a')
        title = info[0].text_content()
        author = info[1].text_content()
        book = {"title": title, "author": author, "rank": number, "length": length}
        books.append(book)
        print(number)
    return books

def get_length(amazon_link):
    try:
        page = req.get(amazon_link)
        tree = html.fromstring(page.content)
        containers = tree.find_class("content")
    # print("area",  containers)
        element = containers[0].cssselect('li')[0].text_content()
        z = re.search("([\d]+)", element)
        z = int(z.group(0)) if z!= None else 0
        return z
    except:
        return 0


    # for k in containers:
    #     print(k.text_content())
import csv


def get_row(book, header):
    row =[]
    for h in header:
        row.append(book.get(h))
    return row

def output_csv(books):
# flatten the list, then
    header = ['rank', 'title', 'author','length']
    with open('books.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for b in books:
            writer.writerow(get_row(b,header))


        # writer.writerow(["SN", "Name", "Contribution"])










# This will create a list of buyers:
# buyers = tree.xpath('//div[@title="buyer-name"]/text()')
# #This will create a list of prices
# prices = tree.xpath('//span[@class="item-price"]/text()')
if __name__ == "__main__":

    books = scrape()

    print(books)
    output_csv(books)
