import tkinter as tk
from tkinter import ttk
from database import load_products
from knapsack import knapsack


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("AI Clothing Shop")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#e8f4fd")  # Light blue background

        # Style configuration
        style = ttk.Style()
        style.configure("TFrame", background="#e8f4fd")
        style.configure("TLabel", background="#e8f4fd", foreground="#1a365d", font=("Arial", 10, "bold"))
        style.configure("TLabelFrame", background="#e8f4fd", foreground="#1e40af", font=("Arial", 12, "bold"))
        style.configure("TButton", background="#000000", foreground="black", font=("Arial", 12, "bold"))
        style.map("TButton", background=[("active", "#333333")])
        style.configure("TCheckbutton", background="#e8f4fd", foreground="#374151", font=("Arial", 9))
        style.configure("TEntry", font=("Arial", 12))

        self.products = load_products()

        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="🛍️ AI Clothing Shop", font=("Arial", 20, "bold"), foreground="#dc2626")
        title_label.pack(pady=(0, 25))

        # Budget section
        budget_frame = ttk.LabelFrame(main_frame, text="Budżet", padding="10")
        budget_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(budget_frame, text="Podaj swój budżet (w zł):").pack(anchor=tk.W)
        self.budget_entry = ttk.Entry(budget_frame, font=("Arial", 12))
        self.budget_entry.pack(fill=tk.X, pady=(5, 0))

        # Type section
        type_frame = ttk.LabelFrame(main_frame, text="Typ ubrania", padding="10")
        type_frame.pack(fill=tk.X, pady=(0, 10))
        self.type_vars = {}
        types = ["tshirt", "hoodie", "pants", "jacket", "shoes", "shorts"]
        for i, t in enumerate(types):
            var = tk.BooleanVar()
            ttk.Checkbutton(type_frame, text=t.capitalize(), variable=var).grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)
            self.type_vars[t] = var

        # Color section
        color_frame = ttk.LabelFrame(main_frame, text="Kolor", padding="10")
        color_frame.pack(fill=tk.X, pady=(0, 10))
        self.color_vars = {}
        colors = ["black", "white", "red", "blue", "green", "gray", "yellow"]
        for i, c in enumerate(colors):
            var = tk.BooleanVar()
            ttk.Checkbutton(color_frame, text=c.capitalize(), variable=var).grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
            self.color_vars[c] = var

        # Brand section
        brand_frame = ttk.LabelFrame(main_frame, text="Marka", padding="10")
        brand_frame.pack(fill=tk.X, pady=(0, 10))
        self.brand_vars = {}
        brands = ["nike", "adidas", "puma", "reebok", "newbalance", "tommy", "zara", "hm"]
        for i, b in enumerate(brands):
            var = tk.BooleanVar()
            ttk.Checkbutton(brand_frame, text=b.capitalize(), variable=var).grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
            self.brand_vars[b] = var

        # Button
        search_button = ttk.Button(main_frame, text="Znajdź najlepszy zestaw", command=self.search)
        search_button.pack(pady=(10, 20))

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Wyniki", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        self.result = tk.Text(results_frame, height=15, width=70, font=("Courier", 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.result.yview)
        self.result.configure(yscrollcommand=scrollbar.set)
        self.result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


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
