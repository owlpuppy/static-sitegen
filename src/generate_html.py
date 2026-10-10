# static-sitegen src/generate_pages.py

import html

import common
from convert_markdown_block import markdown_to_html_node

# helper functions

def extract_title(markdown: str) -> str:
    markdown_split = markdown.splitlines()
    for line in markdown_split:
        if line.startswith('# '):
            return html.escape(line[2:].strip())
    raise ValueError("top level header is missing from markdown")

# primary functions

def generate_html_doc(template_file: str, markdown_file: str, destination_file: str = '') -> None:

    try:
        with open(markdown_file, "r") as file:
            markdown = file.read()
    except Exception as e:
        common.logger.error(f'{e} - unable to read "{markdown_file}"')
        raise

    try:
        with open(template_file, "r") as file:
            template = file.read()
    except Exception as e:
        common.logger.error(f'{e} - unable to read "{template_file}"')
        raise

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()

    title_placeholder = '{{ Title }}'
    content_placeholder = '{{ Content }}'

    if title_placeholder not in template:
        common.logger.warning(f'"{template_file}" does not contain "{title_placeholder}, title will not be present')

    if content_placeholder not in template:
        common.logger.error(f'"{template_file}" does not contain "{content_placeholder}, content will not be present')
        return

    basepath = common._build_basepath

    html_doc = template.replace(title_placeholder, title)
    html_doc = html_doc.replace(content_placeholder, content)
    html_doc = html_doc.replace('href="/', f'href="{basepath}')
    html_doc = html_doc.replace('src="/', f'src="{basepath}')

    try:
        with open(destination_file, "w") as file_to_write:
            file_to_write.write(html_doc)
            common.logger.info(f'Successfully wrote to "{destination_file}" ({len(html_doc)} characters written)')
    except Exception as e:
        common.logger.error(f'{e} - unable to write contents')
        raise
