# src/markdown.py

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    #If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
    #If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
    #The .split() string method was useful
    #The .extend() list method was useful
    # ** for bold, _ for italic, and a backtick for code
    new_nodes = []

    if text_type is not TextType.TEXT:
        for node in old_nodes:
            node_split = node.text.split(delimiter)
            count = len(node_split)
            if count == 1:
                new_nodes.append(node)
            elif count > 2 and count % 2 != 0:
                i = 1
                for subnode in node_split:
                    if subnode != '':
                        if i % 2 != 0:
                            new_nodes.append(TextNode(subnode, node.text_type))
                        else:
                             new_nodes.append(TextNode(subnode, text_type))
                    i += 1
            else:
                raise TypeError(f'syntax error, closing "{delimiter}" not found')
    else:
        new_nodes.extend(old_nodes)

    return new_nodes
