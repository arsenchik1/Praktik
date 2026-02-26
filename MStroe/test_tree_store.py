from tree_store import TreeStore

# Тестовые данные
items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

ts = TreeStore(items)

# Проверка
print("1. getAll():")
print(ts.getAll())
print("\n2. getItem(7):")
print(ts.getItem(7))
print("\n3. getChildren(4):")
print(ts.getChildren(4))
print("\n4. getChildren(5):")
print(ts.getChildren(5))
print("\n5. getAllParents(7):")
print(ts.getAllParents(7))