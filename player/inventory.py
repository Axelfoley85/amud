class Inventory:
    def __init__(self, slot_limit=5, weight_limit=20):
        self.items = []  # each item is dict: {"name": str, "weight": int, "qty": int}
        self.slot_limit = slot_limit
        self.weight_limit = weight_limit

    def total_weight(self):
        return sum(item["weight"] * item["qty"] for item in self.items)

    def add_item(self, name, weight, qty=1):
        for item in self.items:
            if item["name"] == name:
                if self.total_weight() + weight * qty > self.weight_limit:
                    return f"Ye can't carry more than {self.weight_limit} weight units."
                item["qty"] += qty
                return f"Ye pick up {qty} {name}{'s' if qty>1 else ''}."

        if len(self.items) >= self.slot_limit:
            return f"Ye can't carry more than {self.slot_limit} items."
        if self.total_weight() + weight * qty > self.weight_limit:
            return f"Ye can't carry more than {self.weight_limit} weight units."
        self.items.append({"name": name, "weight": weight, "qty": qty})
        return f"Ye pick up {qty} {name}{'s' if qty>1 else ''}."

    def remove_item(self, name, qty=1):
        for item in self.items:
            if item["name"] == name:
                if item["qty"] > qty:
                    item["qty"] -= qty
                    return f"Ye drop {qty} {name}{'s' if qty>1 else ''}."
                elif item["qty"] == qty:
                    self.items.remove(item)
                    return f"Ye drop {qty} {name}{'s' if qty>1 else ''}."
                else:
                    return f"Ye don't have that many {name}s."
        return f"Ye don't have a {name}."

    def list_items(self):
        if not self.items:
            return "Yer inventory be empty."
        out = "In yer inventory:\n"
        for item in self.items:
            out += f"- {item['name']} x{item['qty']} (weight {item['weight']})\n"
        out += f"Total weight: {self.total_weight()} / {self.weight_limit}\n"
        out += f"Slots used: {len(self.items)} / {self.slot_limit}"
        return out

    def upgrade(self, slot_increase=0, weight_increase=0):
        self.slot_limit += slot_increase
        self.weight_limit += weight_increase
        return f"Yer carryin’ capacity has been upgraded!"
