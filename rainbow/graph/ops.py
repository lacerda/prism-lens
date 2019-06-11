"""
Implementations of graph.OpFactory
"""


class Session:
    def __init__(self, ops):
        self.ops = ops

    def clear(self):
        for op in self.ops:
            op.clear()

    def __next__(self):
        results = [op.get_result() for op in self.ops]
        self.clear()
        return results

    def __iter__(self):
        return self


class OpFactory:
    """
    Much like Tensorflow ops, instantiate class with options to define object.
    Call the instance with a preceding Op to add it as a dependency.
    """

    def __call__(self, parents):
        if parents is None:
            parents = tuple([])
        elif not isinstance(parents, (list, tuple)):
                parents = tuple([parents])
        else:
            parents = tuple(parents)

        op = Op(parents, self.operation)
        return op

    # def _get_depth(self):
    #     if not self.parents:
    #         return 0
    #     else:
    #         return max(parent.depth for parent in self.parents) + 1

    def operation(self, _input):
        raise NotImplementedError("This logic needs to be implemented in the custom class")


class Op:
    def __init__(self, parents, operation):
        self.parents = parents
        self.operation = operation
        self.computed = False
        self.result = None

    def clear(self):
        self.computed = False
        for parent in self.parents:
            parent.clear()

    def get_result(self):
        if not self.computed:
            _input = [parent.get_result() for parent in self.parents]
            self.result = self.operation(*_input)
            self.computed = True
        return self.result


class Input(OpFactory):
    """
    Gets input from an iterator.
    """
    def __init__(self, iterator):
        self.iterator = iterator

    def __call__(self):   # Parents are allowed to be None here
        op = super().__call__(None)
        return op

    def operation(self):  # _input should be nothing
        _output = next(self.iterator)
        return _output


class Selector(OpFactory):
    def __init__(self, index):
        self.index = index

    def operation(self, _input):
        _output = _input[self.index]
        return _output


class CV2Function(OpFactory):
    """
    Applies a wrapped CV2 function to input.
    Function should be a partial CV2 function.
    """
    def __init__(self, function):
        self.function = function

    def operation(self, *_input):
        _output = self.function(*_input)
        return _output


class BufferWrite(OpFactory):
    """
    Writes to a buffer.
    """
    def __init__(self, buffer):
        self.buffer = buffer

    def operation(self, _input):
        self.buffer.write(_input)
        return self.buffer


class BufferRead(OpFactory):
    """
    Reads a buffer.
    """
    def __init__(self, buffer):
        self.buffer = buffer

    def operation(self, _input):
        result = self.buffer.read()
        return result


class BufferMoveHead(OpFactory):
    """
    Moves a buffer's head.
    The callback will retrieve the appropriate value.
    """
    def __init__(self, buffer, move_callback):
        self.buffer = buffer
        self.move_callback = move_callback

    def operation(self, _input):
        move_by = self.move_callback()
        self.buffer.move_head(move_by)
        return self.buffer


class BufferSetHead(OpFactory):
    """
    Sets a buffer's head to a position.
    The callback will retrieve the appropriate value.
    """

    def __init__(self, buffer, set_callback):
        self.buffer = buffer
        self.set_callback = set_callback

    def operation(self, _input):
        set_position = self.set_callback()
        self.buffer.set_head(set_position)
        return self.buffer


class MultiBufferWrite(OpFactory):
    """
    Writes to a multibuffer.
    """
    def __init__(self, multibuffer):
        self.multibuffer = multibuffer

    def operation(self, _input):
        self.multibuffer.write(_input)
        return self.multibuffer


class MultiBufferRead(OpFactory):
    """
    Reads a multibuffer.
    """
    def __init__(self, multibuffer):
        self.multibuffer = multibuffer

    def operation(self, _input):
        result = self.multibuffer.read()
        return result


class MultiBufferMoveHeads(OpFactory):
    """
    Moves a multibuffer's head.
    The callback will retrieve the appropriate value.
    """
    def __init__(self, multibuffer, move_callback):
        self.multibuffer = multibuffer
        self.move_callback = move_callback

    def operation(self, _input):
        move_by = self.move_callback()
        self.multibuffer.move_heads(move_by)
        return self.multibuffer


class MultiBufferSetHeads(OpFactory):
    """
    Sets a multibuffer's head to a position.
    The callback will retrieve the appropriate value.
    """

    def __init__(self, multibuffer, set_callback):
        self.multibuffer = multibuffer
        self.set_callback = set_callback

    def operation(self, _input):
        set_position = self.set_callback()
        self.multibuffer.set_heads(set_position)
        return self.multibuffer