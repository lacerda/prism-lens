class Device:
    """
    Devices must be iterators: Implement .__next__ and .__iter__
    """
    def __next__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def run(self):
        """
        This is needed for compatibility with graph.Op
        :return:
        """
        return self.__next__()