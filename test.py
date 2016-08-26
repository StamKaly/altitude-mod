class something:
    def __init__(self):
        self.something = "something"

    def one(self):
        print(self.two())

    def two(self):
        return self.something

something().one()