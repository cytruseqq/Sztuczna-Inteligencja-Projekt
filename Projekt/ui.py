import tkinter as tk
from database import load_products
from knapsack import knapsack


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("AI Clothing Shop")

        self.products = load_products()

        # -------- BUDZET --------

        tk.Label(root, text="Budzet").pack()

        self.budget_entry = tk.Entry(root)
        self.budget_entry.pack()

        # -------- TYP --------

        tk.Label(root, text="Typ ubrania").pack()

        self.type_vars = {}

        types = ["tshirt","hoodie","pants","jacket","shoes","shorts"]

        for t in types:
            var = tk.BooleanVar()
            tk.Checkbutton(root, text=t, variable=var).pack()
            self.type_vars[t] = var

        # -------- KOLOR --------

        tk.Label(root, text="Kolor").pack()

        self.color_vars = {}

        colors = ["black","white","red","blue","green","gray","yellow"]

        for c in colors:
            var = tk.BooleanVar()
            tk.Checkbutton(root, text=c, variable=var).pack()
            self.color_vars[c] = var

        # -------- MARKA --------

        tk.Label(root, text="Marka").pack()

        self.brand_vars = {}

        brands = ["nike","adidas","puma","reebok","newbalance","tommy","zara","hm"]

        for b in brands:
            var = tk.BooleanVar()
            tk.Checkbutton(root, text=b, variable=var).pack()
            self.brand_vars[b] = var

        # -------- BUTTON --------

        tk.Button(
            root,
            text="Znajdz najlepszy zestaw",
            command=self.search
        ).pack()

        # -------- WYNIK --------

        self.result = tk.Text(root,height=20,width=70)
        self.result.pack()


    def search(self):

        budget = int(self.budget_entry.get())

        selected_types = [
            t for t,v in self.type_vars.items() if v.get()
        ]

        selected_colors = [
            c for c,v in self.color_vars.items() if v.get()
        ]

        selected_brands = [
            b for b,v in self.brand_vars.items() if v.get()
        ]

        filtered = []

        for p in self.products:

            if selected_types and p["type"] not in selected_types:
                continue

            if selected_colors and p["color"] not in selected_colors:
                continue

            if selected_brands and p["brand"] not in selected_brands:
                continue

            filtered.append(p)

        best = knapsack(filtered, budget)

        self.result.delete(1.0, tk.END)

        total_price = 0
        total_value = 0

        for item in best:

            self.result.insert(
                tk.END,
                f"{item['name']} | {item['brand']} | {item['color']} | {item['price']} zl\n"
            )

            total_price += item["price"]

        self.result.insert(tk.END, f"\nSUMA: {total_price} zl\n")
