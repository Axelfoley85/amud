class Room:
    def __init__(self, name, desc, items=None, features=None):
        self.name = name
        self.desc = desc
        self.exits = {}
        self.items = items if items else []
        self.features = features if features else []

    def describe(self):
        exits = ', '.join(self.exits.keys())
        item_list = [i["name"] for i in self.items]
        features_list = [f for f in self.features]
        details = []
        if item_list:
            details.append("Ye see here: " + ", ".join(item_list))
        if features_list:
            details.append("There be: " + ", ".join(features_list))
        extra = "\n".join(details)
        return f"{self.name}\n{self.desc}\n{extra}\n  Obvious exits: {exits}"

    def take_item(self, name):
        for item in self.items:
            if item["name"] == name:
                self.items.remove(item)
                return item
        return None

    def drop_item(self, item):
        self.items.append(item)
