import logging

logger = logging.getLogger(__name__)


def _print_node(node, curr_depth: int):
    num_children = len(node)
    text = node.text or ""
    prefix = "  " * curr_depth

    if not isinstance(node.tag, str):
        logging.debug(f"found invalid node with type {type(node.tag)}, skipping")
        assert num_children == 0, f"cant skip, node has {num_children} children"
        return

    print(
        f"{prefix}{node.tag: >10} | {num_children:>4} children | "
        f"{len(text):>6} len text | {len(node.attrib):>2} attributes"
    )


def print_tree(root, curr_depth: int = 0):
    if curr_depth > 10:
        return
    _print_node(root, curr_depth)
    for node in root:
        print_tree(node, curr_depth + 1)
