import csv


def load_products():

    products = []

    with open("clothes.csv", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            products.append({
                "name": row["name"],
                "price": int(row["price"]),
                "value": int(row["value"]),
                "type": row["type"],
                "color": row["color"],
                "brand": row["brand"]
            })

    return products