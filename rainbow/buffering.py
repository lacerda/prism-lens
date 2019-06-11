import numpy as np


class Buffer:
    """
    Interface for a stack of limited size, with a reversed index.
    Append with .write, read with .read, rewrite with .rewrite
    """
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.stack = []
        self.head = 0

    @staticmethod
    def _get_stack_index(position: int):
        index = -(position + 1)
        return index

    def read(self):
        index = self._get_stack_index(position=self.head)
        item = self.stack[index]
        return item

    def write(self, item):
        if len(self.stack) == self.max_size:
            pop = self.stack.pop(0)
        self.stack.append(item)

    def rewrite(self, item):
        index = self._get_stack_index(self.head)
        self.stack[index] = item

    def move_head(self, increment: int):
        requested_position = self.head + increment
        return self.set_head(requested_position)

    def set_head(self, requested_position: int):
        new_head = min(requested_position, len(self.stack) - 1)
        self.head = new_head
        return self.head


class MultiBuffer:
    """
    Manages a set of movable buffers
    """
    def __init__(self, num_buffers=0, buffers_size=None):
        # TODO: Manage buffer heads, avoid calling set_head on each at every iteration.
        self.buffers = []
        # self.heads = np.array([])
        for _ in range(num_buffers):
            buffer = Buffer(buffers_size)
            self.add_buffer(buffer)

    def add_buffer(self, buffer):
        self.buffers.append(buffer)
        # self.heads = np.append([buffer.head])

    def read(self):
        _output = [buffer.read() for buffer in self.buffers]
        return _output

    def write(self, items):
        for buffer, item in zip(self.buffers, items):
            buffer.write(item)

    def set_heads(self, positions):
        """
        Sets the positions of multiple buffers.
        :param positions: iter(int) or dict(name:int). NOP if position is -1.
        :return: bool indicating success of all
        """
        for buffer, position in zip(self.buffers, positions):
            buffer.set_head(position)

    def move_heads(self, increments):
        """
        Moves heads of multiple buffers.
        :param increments: iter(int) or dict(name:int). NOP if increment is 0.
        :return: bool indicating success of all
        """
        for buffer, increment in zip(self.buffers, increments):
            buffer.move_head(increment)


class NumpyBuffer(Buffer):
    """
    Stacks written numpy arrays. Reads from objects according to a multi-head.
    """
    def __init__(self, max_size, object_length):
        super().__init__(max_size)

    def read(self):
        index = self._get_stack_index(position=self.head)
        item = self.stack[index]
        return item

    def write(self, item):
        if len(self.stack) == self.max_size:
            pop = self.stack.pop(0)
        self.stack.append(item)

    def rewrite(self, item):
        index = self._get_stack_index(self.head)
        self.stack[index] = item

    def move_head(self, increment: int):
        requested_position = self.head + increment
        return self.set_head(requested_position)

    def set_head(self, requested_position: int):
        new_head = min(requested_position, len(self.stack) - 1)
        self.head = new_head
        return self.head





