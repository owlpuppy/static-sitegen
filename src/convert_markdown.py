# src/markdown.py

import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    #If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
    #If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
    #The .split() string method was useful
    #The .extend() list method was useful
    # ** for bold, _ for italic, and a backtick for code
    # delimiter: str was removed from the center
    new_nodes = []

    delimiter = ""
    match text_type:
        case TextType.BOLD:
            delimiter = "**"
        case TextType.ITALIC:
            delimiter = "_"
        case TextType.CODE:
            delimiter = "`"
        case TextType.TEXT:
            new_nodes.extend(old_nodes)
            return new_nodes
        case _:
            raise TypeError(f"TextType {text_type} not implemented for split_nodes_delimiter")


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

    return new_nodes

def extract_markdown_images(text):
    padded_text = ' ' + text + ' '
    matches = re.findall(r"(?<=!)\[(.*?)\]\((.*?)\)", padded_text)
    return matches

def extract_markdown_links(text):
    padded_text = ' ' + text + ' '
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", padded_text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        node_raw = node.text
        node_images = extract_markdown_images(node_raw)
        node_image_count = len(node_images)
        if node_image_count == 0:
            new_nodes.append(node)
        else:
            for i in range(node_image_count):
                image_alt = node_images[i][0]
                image_link = node_images[i][1]
                node_sections = node_raw.split(f"![{image_alt}]({image_link})", 1)
                if node_sections[0] != '':
                    new_nodes.append(TextNode(node_sections[0], node.text_type))
                new_nodes.append(TextNode(image_alt, TextType.IMG, image_link))
                node_raw = node_sections[1]
            if node_raw != '':
                new_nodes.append(TextNode(node_raw, node.text_type))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        node_raw = node.text
        node_links = extract_markdown_links(node_raw)
        node_link_count = len(node_links)
        if node_link_count == 0:
            new_nodes.append(node)
        else:
            for i in range(node_link_count):
                link_text = node_links[i][0]
                link_address = node_links[i][1]
                node_sections = node_raw.split(f"[{link_text}]({link_address})", 1)
                if node_sections[0] != '':
                    new_nodes.append(TextNode(node_sections[0], node.text_type))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_address))
                node_raw = node_sections[1]
            if node_raw != '':
                new_nodes.append(TextNode(node_raw, node.text_type))
    return new_nodes

# primary function

def text_to_textnodes(text) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    processed_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(text_nodes)), TextType.CODE), TextType.ITALIC), TextType.BOLD)
    return processed_nodes


# image regex: !\[(.*?)\]\((.*?)\)
# link regex: [^!]\[(.*?)\]\((.*?)\)
# new link regex (?<!^!)\[(.*?)\]\((.*?)\)
# new new link regex (?<!!)\[(.*?)\]\((.*?)\)
