import csv
import random

types = [
    "tshirt",
    "hoodie",
    "pants",
    "jacket",
    "shoes",
    "shorts"
]

colors = [
    "black",
    "white",
    "red",
    "blue",
    "green",
    "gray",
    "yellow"
]

brands = [
    "nike",
    "adidas",
    "puma",
    "reebok",
    "newbalance",
    "tommy",
    "zara",
    "hm"
]


def generate_products(n=10000):

    with open("clothes.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "id",
            "name",
            "price",
            "value",
            "type",
            "color",
            "brand"
        ])

        for i in range(1, n + 1):

            type_choice = random.choice(types)
            color_choice = random.choice(colors)
            brand_choice = random.choice(brands)

            price = random.randint(30, 600)

            value = price + random.randint(10, 200)

            name = f"{brand_choice}_{type_choice}_{i}"

            writer.writerow([
                i,
                name,
                price,
                value,
                type_choice,
                color_choice,
                brand_choice
            ])


if __name__ == "__main__":
    generate_products(10000)