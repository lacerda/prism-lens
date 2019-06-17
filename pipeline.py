import time


class Clock:
    def __init__(self):
        self._tic = None     # initial timeframe
        self._tictoc = None  # time between tic and toc
        self._toctic = None  # fps
    def tic(self):
        self._tic = time.time()
    def toc(self):
        self._tictoc = time.time() - self._tic
        self._toctic = 1 / self._tictoc
    def tictoc(self):
        return self._tictoc
    def toctic(self):
        return self._toctic


class Pipeline:
    """
    Iterator. input from devices, sends them to any processors, returns the transformed input.
    Flow:
    - process commands
    - capture from devices
    - process graph
    - return output
    """
    def __init__(self, device, graph):
        self.clock = Clock()
        self.device = device
        self.graph = graph
        self.commands

        self._dry_run()  # After the pipeline is defined

    def _dry_run(self):
        # Gets a baseline for performance
        self.__next__()

    def send_command(self, cmd):
        pass

    def _process_commands(self):
        pass

    def _process_graph(self):
        pass

    def _run_pipeline(self):
        self._process_commands()
        self._process_graph()

    def __iter__(self):
        return self

    def __next__(self):
        self.tic()
        self._run_pipeline()
        self.toc()