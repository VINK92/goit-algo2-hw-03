import csv
from BTrees.OOBTree import OOBTree
import timeit

# Читання даних з CSV файлу
def load_data(file_path):
    data = []
    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["ID"] = int(row["ID"])
            row["Price"] = float(row["Price"])
            data.append(row)
    return data

# Додавання товарів до OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }

# Додавання товарів до словника
def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }

# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    return [
        value for _, value in tree.items()
        if min_price <= value["Price"] <= max_price
    ]

# Діапазонний запит для словника
def range_query_dict(dictionary, min_price, max_price):
    return [
        value for value in dictionary.values()
        if min_price <= value["Price"] <= max_price
    ]

def main():
    file_path = "generated_items_data.csv"
    data = load_data(file_path)

    # Ініціалізація структур
    tree = OOBTree()
    dictionary = {}

    # Додавання даних до структур
    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначення діапазону цін для тестування
    min_price = 10.0
    max_price = 50.0

    # Вимірювання продуктивності OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price), number=100
    )

    # Вимірювання продуктивності Dict
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price), number=100
    )

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()
