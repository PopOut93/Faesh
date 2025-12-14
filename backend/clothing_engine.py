from avatar_engine import Avatar

class ClothingItem:
    def __init__(self, name, category, size):
        self.name = name
        self.category = category
        self.size = size

class ClothingEngine:
    def __init__(self):
        self.items_db = []

    def add_item(self, item: ClothingItem):
        self.items_db.append(item)
        return f"{item.name} added to database"

    def try_on(self, avatar: Avatar, item_name: str):
        item = next((i for i in self.items_db if i.name == item_name), None)
        if item:
            return avatar.add_clothing_item(item.name)
        else:
            return f"Item {item_name} not found"
