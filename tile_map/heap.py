from tile_map.tile import Tile

# Heap sort implementation
class Heap:

    def __init__(self):
        self.items = []
        self.last_index = 0

    def __contains__(self, item):
        if item.heap_index >= len(self.items):
            return False
        return self.items[item.heap_index] == item

    def add(self, item: Tile):
        item.heap_index = self.last_index
        if self.last_index >= len(self.items):
            self.items.append(item)
        else:
            self.items[item.heap_index] = item

        self.sort_up(item)
        self.last_index += 1

    def pop(self):
        item = self.items[0]
        self.last_index -= 1
        self.items[0] = self.items[self.last_index]
        self.items[0].heap_index = 0
        self.sort_down(self.items[0])
        return item

    def update(self, item: Tile):
        self.sort_up(item)

    def sort_down(self, item: Tile):
        while True:
            left_child_index = (item.heap_index * 2) + 1
            right_child_index = (item.heap_index * 2) + 2

            if left_child_index < self.last_index:
                swap_index = left_child_index

                if right_child_index < self.last_index:
                    if self.items[right_child_index] < self.items[left_child_index]:
                        swap_index = right_child_index

                if self.items[swap_index] < item:
                    self.swap(item, self.items[swap_index])
                else:
                    return
            else:
                return

    def sort_up(self, item: Tile):
        parent_index = int((item.heap_index - 1)/2)

        while True:
            parent = self.items[parent_index]
            if item < parent:
                self.swap(parent, item)
            else:
                return

            parent_index = int((item.heap_index - 1)/2)

    def swap(self, item1: Tile, item2: Tile):
        self.items[item1.heap_index] = item2
        self.items[item2.heap_index] = item1

        item1_index = item1.heap_index
        item1.heap_index = item2.heap_index
        item2.heap_index = item1_index
