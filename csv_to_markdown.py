


import csv



f = "books.csv"



def make_row(data):
    string = "|"
    for d in data:
        string += f"{str(d)} |"
    return string + "\n"



def make_header(data):
    string = "|"
    for d in data:
        string += f"---- |"
    return string + "\n"

def to_md():
    markdown_string = ""
    with open("books.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        first = True
        for row in csv_reader:
            if first:
                first = False
                markdown_string += make_row(row)
                markdown_string += make_header(row)
            else:
                markdown_string += make_row(row)
    f = open("README.md", "w")
    f.write(markdown_string)
    f.close()

to_md()

