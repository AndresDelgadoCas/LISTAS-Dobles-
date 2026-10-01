from horse import Horse


class HorseNode:
    """Node used by the doubly linked list."""

    def __init__(self, horse):
        self.horse = horse
        self.previous = None
        self.next = None


class DoublyLinkedList:
    """Doubly linked list used to manage horse records."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def add(self, horse):
        new_node = HorseNode(horse)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.current = new_node
        self.size += 1

    def find(self, horse_id):
        node = self.head

        while node:
            if node.horse.horse_id.lower() == horse_id.lower():
                return node
            node = node.next

        return None

    def delete(self, horse_id):
        node = self.find(horse_id)

        if node is None:
            return False

        if node.previous:
            node.previous.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.previous = node.previous
        else:
            self.tail = node.previous

        if self.current == node:
            self.current = node.next if node.next else node.previous

        self.size -= 1

        if self.size == 0:
            self.current = None

        return True

    def update(self, horse_id, name, breed, age, owner, health, training):
        node = self.find(horse_id)

        if node is None:
            return False

        node.horse.name = name
        node.horse.breed = breed
        node.horse.age = age
        node.horse.owner = owner
        node.horse.health = health
        node.horse.training = training

        return True

    def next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return True
        return False

    def previous(self):
        if self.current and self.current.previous:
            self.current = self.current.previous
            return True
        return False

    def forward(self):
        horses = []
        node = self.head

        while node:
            horses.append(node.horse)
            node = node.next

        return horses

    def backward(self):
        horses = []
        node = self.tail

        while node:
            horses.append(node.horse)
            node = node.previous

        return horses
