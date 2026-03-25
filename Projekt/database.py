"""
Moduł bazy danych dla SmartSearch AI.
Odpowiada za wczytywanie i przetwarzanie danych produktów z pliku CSV.
"""

import csv
from typing import List, Dict, Any


def load_products() -> List[Dict[str, Any]]:
    """
    Wczytuje produkty z pliku clothes.csv do struktury słownika.
    
    Returns:
        Lista słowników zawierających dane produktów:
        - name: Nazwa produktu (str)
        - price: Cena (int, w PLN)
        - value: Wartość estetyczna (int, 0-1000)
        - type: Kategoria (str, np. 'jacket', 'shoes')
        - color: Kolor (str)
        - brand: Marka (str)
    
    Raises:
        FileNotFoundError: Jeśli plik clothes.csv nie istnieje
        ValueError: Jeśli CSV ma niepoprawny format
    """
    products: List[Dict[str, Any]] = []

    try:
        with open("clothes.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no headers")
            
            for row in reader:
                if row is None:
                    continue
                    
                try:
                    products.append({
                        "name": row["name"],
                        "price": int(row["price"]),
                        "value": int(row["value"]),
                        "type": row["type"],
                        "color": row["color"],
                        "brand": row["brand"]
                    })
                except (KeyError, ValueError) as e:
                    raise ValueError(f"Invalid row format in CSV: {e}") from e
    
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "clothes.csv file not found. Make sure it exists in the application directory."
        ) from e

    return products