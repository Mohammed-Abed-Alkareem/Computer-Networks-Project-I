def read_file(file_name):

    file = open(file_name, "r")

    name = []
    price = []

    for line in file:
        split_line = line.split("#")
        name.append(split_line[0])
        price.append(int(split_line[1].split("\n")[0]))

    file.close()

    return [name, price]


def sort_by_name(name_price):
    name = name_price[0]
    price = name_price[1]

    n = len(name)

    for i in range(n-1):
        for j in range(n-i-1):
            if name[j] > name[j + 1]:
                name[j], name[j + 1] = name[j + 1], name[j]
                price[j], price[j + 1] = price[j + 1], price[j]


def sort_by_price(name_price):
    name = name_price[0]
    price = name_price[1]

    n = len(name)

    for i in range(n-1):
        for j in range(n-i-1):
            if price[j] < price[j + 1]:
                name[j], name[j + 1] = name[j + 1], name[j]
                price[j], price[j + 1] = price[j + 1], price[j]




# if __name__ == "__main__":
#     name_price = read_file("HTML_Files/Text_Files/laptops.txt")
#     sort_by_name(name_price)
#     print(name_price)
#     sort_by_price(name_price)

