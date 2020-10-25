class Node:
    def __init__(self, priority, puzzle_state):
        self.priority = priority
        self.puzzle_state = puzzle_state

    def __repr__(self):
        return f'({self.priority}, {self.puzzle_state})'


class PriorityQueue:

    """     Minimum Priority Queue      """

    def __init__(self):
        self.queue_len = 0
        self.queue = list()

    def __repr__(self):
        return str(self.queue)

    def add(self, priority: int, puzzle_state):
        """     Insert to queue in ASCENDING Order      """
        node = Node(priority=priority, puzzle_state=puzzle_state)
        i = 0
        # -- Insertions -- #
        while i < self.queue_len:
            if priority < self.queue[i].priority:
                self.queue.insert(i, node)
                self.queue_len += 1
                return
            elif priority == self.queue[i].priority:
                # -- Maintain IN-LINE property of Algorithm -- #
                self.queue.insert(i+1, node)
                self.queue_len += 1
                return
            i += 1
        # -- Appends to END -- #
        self.queue.append(node)
        self.queue_len += 1

    def append(self, puzzle_state):
        node = Node(priority=-1, puzzle_state=puzzle_state)
        self.queue.append(node)
        self.queue_len += 1

    def pop(self):
        """     Return Item with Lowest Priority   """
        self.queue_len -= 1
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        """     Returns True if queue is empty, False otherwise     """
        return self.queue_len == 0



def test():
    """     TESTING FUNCTION        """
    import random
    items = [
        (random.randint(1, 100), 'a'),
        (random.randint(1, 100), 'b'),
        (random.randint(1, 100), 'c'),
        (random.randint(1, 100), 'd'),
        (60, 'e'), (60, 'f'),  # test inplace property of algo
    ]
    print(f'DEBUG: items {str(items)}')
    pq = PriorityQueue()
    while items:
        item = items.pop(0)
        pq.add(*item)
    print(f'DEBUG: priority_queue {pq}')


if __name__ == '__main__':
    # -- Calls only for testing -- #
    test()
