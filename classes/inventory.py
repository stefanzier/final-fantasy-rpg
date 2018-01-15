# Item Class - for use within a Person's "Items" menu
class Item:
    # Initialize our Item
    def __init__(self, name, type, description, prop):
        self.name = name
        self.type = type
        self.description = description
        self.prop = prop

