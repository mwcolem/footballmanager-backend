class Player:
    def __init__(self, name):
        self.name = name
        self.ppr_position_tier = -1
        self.ppr_flex_tier = -1
        self.half_position_tier = -1
        self.half_flex_tier = -1
        self.standard_position_tier = -1
        self.standard_flex_tier = -1

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
