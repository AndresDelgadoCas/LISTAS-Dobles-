class Horse:
    """Represents a horse managed by the stable."""

    def __init__(self, horse_id, name, breed, age, owner, health, training):
        self.horse_id = horse_id
        self.name = name
        self.breed = breed
        self.age = age
        self.owner = owner
        self.health = health
        self.training = training

    def __repr__(self):
        return f"Horse({self.horse_id}, {self.name})"
