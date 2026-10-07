# static-sitegen src/generate_pages.py

import os
import shutil
import logging

from convert_markdown_block import markdown_to_html_node

ABSPATH = os.path.abspath("./")

logging.basicConfig(
    filename=os.path.join(ABSPATH, "logs", "static_sitegen.log"),      # Name of the log file
    filemode='a',                # 'a' to append, 'w' to overwrite
    format='%(asctime)s %(levelname)s: %(funcName)s: %(message)s',  # Log message format
    level=logging.DEBUG          # Minimum log level to capture
)

# helpers

def html_specialchars_encode(text: str) -> str:
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;").replace("<", "&lt;").replace(">", "&gt;")

# primary functions

def extract_title(markdown: str) -> str:
    markdown = html_specialchars_encode(markdown) # remove this when we take the pages in
    markdown_split = markdown.splitlines()
    for line in markdown_split:
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("top level header is missing from markdown")

def generate_page(from_path: str, template_path: str, dest_path: str = '') -> None:
    logging.info('started')
    destination_root = os.path.join(ABSPATH, 'public')
    markdown_root = 'content'
    markdown_source = os.path.join(ABSPATH, markdown_root, from_path)
    markdown_src_ext = '.md'
    template_source = os.path.join(ABSPATH, template_path)
    template_src_ext = '.html'
    html_destination = os.path.join(destination_root, dest_path)
    destination_file = os.path.join(html_destination, os.path.basename(markdown_source).replace(markdown_src_ext, template_src_ext))

    print(f'Generating page from {from_path} to {dest_path} using {template_path} as template...')
    logging.info(f'Generating page from {markdown_source} to {html_destination} using {template_source} as template...')

    if markdown_source.endswith(markdown_src_ext) and os.path.isfile(markdown_source):
        try:
            with open(markdown_source, "r") as file:
                markdown = file.read()
                #markdown = html_specialchars_encode(markdown)
                logging.info(f'reading markdown source "{markdown_source}"...')
        except Exception as e:
            logging.error(f'{e} - unable to read "{markdown_source}"')
            raise
    else:
        logging.error(f'"{markdown_source}" does not exist, is not a file, or is not a file of type "{markdown_src_ext}".')
        raise ValueError(f'"{from_path}" does not exist, is not a file, or is not a file of type "{markdown_src_ext}".')

    if template_source.endswith(template_src_ext) and os.path.isfile(template_source):
        try:
            with open(template_source, "r") as file:
                template = file.read()
                logging.info(f'reading template source "{template_source}"...')
        except Exception as e:
            logging.error(f'{e} - unable to read "{template_source}"')
            raise
    else:
        logging.error(f'"{template_source}" does not exist, is not a file, or is not a file of type "{template_src_ext}"')
        raise ValueError(f'"{template_path}" does not exist, is not a file, or is not a file of type "{template_src_ext}"')

    if html_destination.startswith(destination_root):
        if not os.path.isdir(html_destination):
            try:
                os.makedirs(html_destination)
                print(f'destination not present, creating "{dest_path}" directories')
                logging.info(f'"{html_destination}" not present, creating "{dest_path}" directories')
            except Exception as e:
                logging.error(f'{e}, unable to create directories for path "{html_destination}"')
                raise
    else:
        logging.error(f'"{html_destination}" does not include required "{destination_root}"')
        raise ValueError(f'"{html_destination}" does not include required "{destination_root}"')

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()

    html_doc = template.replace('{{ Title }}', title)
    html_doc = html_doc.replace('{{ Content }}', content)
    logging.info("generating html, adding to template...")

    try:
        with open(destination_file, "w") as file_to_write:
            file_to_write.write(html_doc)
            logging.info(f'Successfully wrote to "{destination_file}" ({len(html_doc)} characters written)')
    except Exception as e:
        logging.error(f'{e} - unable to write contents')
        raise

    logging.info(f'done')
