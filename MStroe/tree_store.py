class TreeStore:
    def __init__(self, items):
        self.items = items
        # Для быстрого поиска по id
        self.items_by_id = {item["id"]: item for item in items}
        # Для быстрого поиска детей
        self.children_by_parent = {}
        for item in items:
            parent = item["parent"]
            if parent not in self.children_by_parent:
                self.children_by_parent[parent] = []
            self.children_by_parent[parent].append(item)

    def getAll(self):
        return self.items

    def getItem(self, id):
        return self.items_by_id.get(id)

    def getChildren(self, id):
        return self.children_by_parent.get(id, [])

    def getAllParents(self, id):
        parents = []
        current_id = id
        
        while current_id in self.items_by_id:
            current_item = self.items_by_id[current_id]
            parent_id = current_item["parent"]
            
            if parent_id == "root" or parent_id not in self.items_by_id:
                break
                
            parents.append(self.items_by_id[parent_id])
            current_id = parent_id
            
        return parents