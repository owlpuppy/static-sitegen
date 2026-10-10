# static-sitegen src/file_operations.py

import os
import shutil

import common
from generate_html import generate_html_doc

# fileops statics

BUILD_DEST = 'docs'
TEST_DEST = 'public'

# helper functions

def dest_dir() -> str:
    return BUILD_DEST if common._build_mode else TEST_DEST

def mode_type() -> str:
    return 'build mode' if common._build_mode else 'test mode'

# file ops functions

def duplicate_files(current_from: str = '', current_to: str = ''):
    source_dir = "static"
    destination_dir = dest_dir()
    msg_from = os.path.join(current_from, source_dir)
    msg_to = os.path.join(current_to, destination_dir)

    if current_from != current_to:
        common.logger.error(f'path mismatch - "{current_from}" != "{current_to}, ending..."')
        raise ValueError(f'path mismatch - "{current_from}" != "{current_to}"')

    write_from = os.path.join(common.ABSPATH, source_dir)
    write_to = os.path.join(common.ABSPATH, destination_dir)

    if current_from != '' and current_to != '':
        write_from = os.path.join(write_from, current_from)
        write_to = os.path.join(write_to, current_to)
    else:
        common.logger.info('started')
        common.console_print('copying static files...', True)
        try:
            old_files = os.listdir(write_to)
            for old_file in old_files:
                to_remove = os.path.join(write_to, old_file)
                if os.path.isfile(to_remove) or os.path.islink(to_remove):
                    os.unlink(to_remove)
                elif os.path.isdir(to_remove):
                    shutil.rmtree(to_remove)
            common.logger.info(f'deleted previous destination contents in "{write_to}"')
            common.console_print(f'deleted previous destination contents in "{destination_dir}"')
        except Exception as e:
            common.logger.error(f'{e}, ending...')
            raise

    try:
        current_files = os.listdir(write_from)
        for file in current_files:
            next = os.path.join(write_from, file)
            if os.path.isfile(next):
                file_to_copy = os.path.join(write_from, file)
                shutil.copy(file_to_copy, write_to)
                common.logger.info(f'copy "{file}" from "{write_from}" to "{write_to}"')
                common.console_print(f'copy "{file}" from "{msg_from}" to "{msg_to}"')
            else:
                new_dir = os.path.join(write_to, file)
                os.mkdir(new_dir)
                common.logger.info(f'make dir in "{write_to}" named "{file}"')
                common.console_print(f'make dir in "{msg_to}" named "{file}"')
                from_next = os.path.join(current_from, file)
                to_next = os.path.join(current_to, file)
                duplicate_files(from_next, to_next)
    except Exception as e:
        common.logger.error(f'{e}, ending...')
        raise

def generate_pages(template_path: str, current_from: str = '', current_to: str = '') -> None:
    source_dir = "content"
    destination_dir = dest_dir()
    markdown_ext = '.md'
    html_ext = '.html'
    template_source = os.path.join(common.ABSPATH, template_path)
    msg_from = os.path.join(source_dir, current_from)
    msg_to = os.path.join(destination_dir, current_to)

    if not os.path.isfile(template_source) and not template_source.endswith(html_ext):
        common.console_print(f'template "{template_path}" is missing or not an HTML file')
        common.logger.error(f'template "{template_source}" is missing or not an HTML file')
        return

    if current_from != current_to:
        common.logger.error(f'path mismatch - "{current_from}" != "{current_to}, ending..."')
        raise ValueError(f'path mismatch - "{current_from}" != "{current_to}"')

    write_from = os.path.join(common.ABSPATH, source_dir)
    write_to = os.path.join(common.ABSPATH, destination_dir)

    if current_from != '' and current_to != '':
        write_from = os.path.join(write_from, current_from)
        write_to = os.path.join(write_to, current_to)
    else:
        common.logger.info('started')
        common.console_print('generating files...', True)

    try:
        current_files = os.listdir(write_from)
        for file in current_files:
            next = os.path.join(write_from, file)
            if os.path.isfile(next):
                if next.endswith(markdown_ext):
                    new_file = file[:-len(markdown_ext)] + html_ext
                    next_destination = os.path.join(write_to, new_file)
                    current_md = os.path.join(msg_from, file)
                    current_html = os.path.join(msg_to, new_file)
                    if not os.path.isdir(write_to):
                        common.console_print(f'{msg_to} not present, creating')
                        os.makedirs(write_to)
                        common.logger.info(f'"{write_to}" not present, creating...')
                    common.console_print(f'Generating page from "{current_md}" to "{current_html}" using "{template_path}" as template...')
                    common.logger.info(f'Generating page from "{next}" to "{next_destination}" using "{template_source}" as template...')
                    generate_html_doc(template_source, next, next_destination)
                else:
                    common.logger.warning('"{next}" is not a markdown file, file ignored')
            else:
                from_next = os.path.join(current_from, file)
                to_next = os.path.join(current_to, file)
                generate_pages(template_path, from_next, to_next)

    except Exception as e:
        common.logger.error(f'{e}, ending...')
        raise

# wrapper

def create_site() -> bool:
    destination_dir = dest_dir()
    destination = os.path.join(common.ABSPATH, destination_dir)
    common.logger.info(f'preparing to create site in {mode_type()}')
    common.console_print('started ---------------------', True)
    if not os.path.isdir(destination):
        try:
            os.mkdir(destination)
            common.logger.info(f'destination "{destination}" not present, creating')
            common.console_print(f'destination "{destination_dir}" not present, creating')
        except Exception as e:
            common.logger.error(f'{e}')
            raise

    duplicate_files()
    generate_pages("template.html")
    common.console_print("done ------------------------\n", True)
    common.logger.info('done')
    return True
