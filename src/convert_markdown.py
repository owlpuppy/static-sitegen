# src/convert_markdown.py

import re
from enum import Enum
from textnode import TextType, TextNode

# common

class BlockType(Enum):
    PARA = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UL = 'unordered_list'
    OL =  'ordered_list'

# split nodes subfunctions

def extract_markdown_images(text: str) -> list[str]:
    padded_text = ' ' + text + ' '
    matches = re.findall(r"(?<=!)\[(.*?)\]\((.*?)\)", padded_text)
    return matches

def extract_markdown_links(text: str) -> list[str]:
    padded_text = ' ' + text + ' '
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", padded_text)
    return matches

# split nodes functions

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
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
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
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
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
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
        if node.text_type is TextType.TEXT:
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
            new_nodes.append(node)

    return new_nodes

# primary function for creating nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    processed_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(text_nodes)), TextType.CODE), TextType.ITALIC), TextType.BOLD)
    return processed_nodes

# block level functions

def markdown_to_blocks(markdown: str) -> list[str]:
    markdown_blocks = []
    markdown_blocks_raw = markdown.split("\n\n")
    for block_raw in markdown_blocks_raw:
        block_raw = block_raw.strip()
        if block_raw != '':
            markdown_blocks.append(block_raw)

    return markdown_blocks

def block_to_block_type(block: str) -> BlockType:

    if re.match(r"^#{1,6} .", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        new_block = block[1:]
        if len(new_block.strip()) > 0:
            return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UL
    if block.startswith("1. "):
        block_split = block.splitlines()
        lines = len(block_split)
        count = 0
        for line in block_split:
            count += 1
            if not line.startswith(f"{count}. "):
                break
        if lines == count:
            return BlockType.OL
    return BlockType.PARA
