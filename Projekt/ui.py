import tkinter as tk
from database import load_products
from knapsack import knapsack


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("AI Clothing Shop")

        self.products = load_products()

        tk.Label(root, text="Budzet").pack()

        self.budget_entry = tk.Entry(root)
        self.budget_entry.pack()

        tk.Label(root, text="Typ ubrania").pack()

        self.type_var = tk.StringVar()

        types = ["tshirt","hoodie","pants","jacket","shoes","shorts"]

        for t in types:
            tk.Radiobutton(
                root,
                text=t,
                variable=self.type_var,
                value=t
            ).pack()

        tk.Button(
            root,
            text="Znajdz najlepszy zestaw",
            command=self.search
        ).pack()

        self.result = tk.Text(root,height=20,width=60)
        self.result.pack()


    def search(self):

        budget = int(self.budget_entry.get())
        selected_type = self.type_var.get()

        filtered = []

        for p in self.products:

            if selected_type == "" or p["type"] == selected_type:
                filtered.append(p)

        best = knapsack(filtered, budget)

        self.result.delete(1.0, tk.END)

        total_price = 0
        total_value = 0

        for item in best:

            self.result.insert(
                tk.END,
                f"{item['name']}  {item['price']} zl\n"
            )

            total_price += item["price"]
            total_value += item["value"]

        self.result.insert(
            tk.END,
            f"\nSUMA: {total_price} zl\n"
        )

        self.result.insert(
            tk.END,
            f"WARTOSC: {total_value}\n"
        )