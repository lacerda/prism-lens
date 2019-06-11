
#
#
# class Graph:
#     """
#     Manages communication between Ops.
#     - An op has dependencies (and is a dependent of its dependencies)
#     - Ops register dependencies
#     - Calls to dependencies output will be accumulated so dependent only runs once within an iteration.
#     - Is an iterator.
#     """
#     def __init__(self, final_ops):
#         self.final_ops = final_ops
#
#     def __next__(self):
#         return [op.get_result() for op in self.final_ops]
#
#     @staticmethod
#     def _find_op_roots(op):
#         if op.is_root:
#             return {op}
#         else:
#             op_roots = set()
#             for parent in op.parents:
#                 op_roots.update(Graph._find_roots(parent))
#             return op_roots


