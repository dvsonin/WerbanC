"""
    Batch iterate transformer methods
"""

from lark import v_args

class BatchIterateMixin:

    @v_args(inline=True)
    @staticmethod
    def item_attr_name(name):
        return str(name)

    @staticmethod
    def item_attr_names(children):
        return tuple(children)

    @staticmethod
    def item_source_tuples(children):
        return tuple(children)

    @v_args(inline=True)
    @staticmethod
    def iterate_block(names, rows):
        if len(set(names)) != len(names):
            raise ValueError(
                f"Fields of batch_iterate must be uniq: {names}"
            )

        items = []

        for index, row in enumerate(rows, start=1):
            if len(row) != len(names):
                raise ValueError(
                    f"batch_iterate: tuple №{index} contains "
                    f"{len(row)} values, wait {len(names)} "
                    f"for fields {names}"
                )

            items.append(dict(zip(names, row, strict=True)))

        return items