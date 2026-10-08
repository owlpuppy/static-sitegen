# static-sitegen src/convert_markdown.py

import re
from enum import Enum

import common

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from convert_markdown_inline import text_to_textnodes

# common

class BlockType(Enum):
    PARA = 'paragraph'
    HEADING = 'heading'
    PRE = 'preformatted_code'
    QUOTE = 'quote'
    UL = 'unordered_list'
    OL =  'ordered_list'

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
        return BlockType.PRE
    if all(line.startswith(">") for line in block.splitlines()):
        new_block = block[1:]
        if len(new_block.strip()) > 0:
            return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UL
    if block.startswith("1. "):
        block_split = block.splitlines()
        count = 1
        for line in block_split:
            if not line.startswith(f"{count}. "):
                return BlockType.PARA
            count += 1
        return BlockType.OL
    return BlockType.PARA

# full generator

def markdown_to_html_node(markdown: str) -> HTMLNode:

    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARA:
                child_nodes = list(map(text_node_to_html_node, text_to_textnodes(block.replace("\n", " "))))
                nodes.append(ParentNode("p", child_nodes))
            case BlockType.HEADING:
                block_split = block.split(" ", 1)
                heading_number = block_split[0].count("#")
                child_nodes = list(map(text_node_to_html_node, text_to_textnodes(block_split[1].strip())))
                nodes.append(ParentNode(f"h{heading_number}", child_nodes))
            case BlockType.PRE:
                child_nodes = [text_node_to_html_node(TextNode(block[4:-3], TextType.CODE))]
                nodes.append(ParentNode("pre", child_nodes))
            case BlockType.QUOTE:
                to_join = []
                for line in block.splitlines():
                    line = line[1:]
                    if line.startswith(" "):
                        line = line[1:]
                    if not line.isspace():
                        to_join.append(line)
                child_nodes = list(map(text_node_to_html_node, text_to_textnodes(" ".join(to_join))))
                nodes.append(ParentNode("blockquote", child_nodes))
            case BlockType.UL:
                child_nodes = []
                list_items = [line[2:] for line in block.splitlines()]
                for item in list_items:
                    item_children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    child_nodes.append(ParentNode("li", item_children))
                nodes.append(ParentNode("ul", child_nodes))
            case BlockType.OL:
                child_nodes = []
                list_items = [line[3:] for line in block.splitlines()]
                for item in list_items:
                    item_children = list(map(text_node_to_html_node, text_to_textnodes(item)))
                    child_nodes.append(ParentNode("li", item_children))
                nodes.append(ParentNode("ol", child_nodes))

    return ParentNode("div", nodes)
