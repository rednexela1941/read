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

# def scrape():
#     books = []
#     for k in range(1,21):
#         link = URL + f"?page={k}"
#         books.append(parse(link))
#     return flatten(books)

def string_html(element):
    el = etree.tostring(element, pretty_print=True)
    return el
# https://thegreatestbooks.org/?page=4

def extract_isbn(amazon_link):
    z = re.search("dp\/([\d]+)", amazon_link)
    z = z.groups()[0]
    return z


def parse():
    books = []
    header = ['rank', 'title', 'author','length']
    with open('books.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for k in range(1,2):
            link = URL + f"?page={k}"
            print(link)
            next
            page = req.get(link)
            tree = html.fromstring(page.content)
            containers = tree.find_class("item pb-3 pt-3 border-bottom")
            for c in containers:
                # print(etree.tostring(k, pretty_print=True))
                element = c.find_class('col')[0].cssselect('h4')[0]
                # print(amazon_link)
                # print(extract_isbn(amazon_link))
                # try:
                try:
                    amazon = c.find_class('pb-3')[0].find_class('pull-left mr-3')[0].cssselect('a')
                    amazon_link = amazon[1].get("href")
                    amazon_isbn = extract_isbn(amazon_link)
                    length = get_rlength(amazon_isbn)
                except:
                    print("couldn't get length")
                    length = 0
                    # break
                # length = get_length(amazon_link)
                # except:
                # print("couldn't get amazon link")
                info = element.text_content()
                split = info.split('.')
                number = int(split[0])
                info = element.cssselect('a')
                title = info[0].text_content()
                author = info[1].text_content()
                book = {"title": title, "author": author, "rank": number, "length": length}
                writer.writerow(get_row(book, header))
                print(number, book)

def get_rlength(isbn):
    link = f"https://www.readinglength.com/book/isbn-{isbn}/"
    page = req.get(link)
    tree = html.fromstring(page.content)
    text = tree.text_content()
    print(text)
    z = re.search("Pages([\d]+)", text)
    # k = re.search("\"wordCount\":([\d]+)",text)

    # print(k.groups())# print(z.groups()[0])
    return int(z.groups()[0])





def get_length(amazon_link):
    page = req.get(amazon_link)
    tree = html.fromstring(page.content)
    print(tree, "tree")
    print(tree.text_content())
    containers = tree.find_class("content")
    # print("area",  containers)
    print(containers)
    element = containers[0].cssselect('li')
    for e in element:
        print(e.text_content())
    return 0


        # print("amazon word count here", element)
        # z = re.search("([\d]+)", element)
        # z = int(z.group(0)) if z!= None else 0
        # return z
    #     return 0
    # except:
    #     print("no word count")
    #     return 0


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

    parse()
    # books = scrape()

    # print(books)
    # output_csv(books)
