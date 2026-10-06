# src/file_operations.py

import os
import shutil
import logging

ABSPATH = os.path.abspath("./")

logging.basicConfig(
    filename=os.path.join(ABSPATH, "logs", "fileops.log"),      # Name of the log file
    filemode='a',                # 'a' to append, 'w' to overwrite
    format='%(asctime)s %(levelname)s: %(funcName)s: %(message)s',  # Log message format
    level=logging.DEBUG          # Minimum log level to capture
)

def duplicate_files(current_from: str = '', current_to: str = ''):
    #it works, now add a log writer first
    source_dir = "static"
    destination_dir = "public"

    if current_from != current_to:
        logging.error(f'path mismatch - "{current_from}" != "{current_to}, ending..."')
        raise ValueError(f'path mismatch - "{current_from}" != "{current_to}"')

    write_from = os.path.join(ABSPATH, source_dir)
    write_to = os.path.join(ABSPATH, destination_dir)

    if current_from != '' and current_to != '':
        print(f'from {current_from}, to {current_to}')
        write_from = os.path.join(write_from, current_from)
        write_to = os.path.join(write_to, current_to)
    else:
        logging.info('started')
        try:
            old_files = os.listdir(write_to)
            for old_file in old_files:
                to_remove = os.path.join(write_to, old_file)
                if os.path.isfile(to_remove) or os.path.islink(to_remove):
                    os.unlink(to_remove)
                elif os.path.isdir(to_remove):
                    shutil.rmtree(to_remove)
            logging.info(f'deleted previous destination contents in "{write_to}"')
        except Exception as e:
            logging.error(f'{e}, ending...')
            raise

    try:
        current_files = os.listdir(write_from)
        for file in current_files:
            next = os.path.join(write_from, file)
            if os.path.isfile(next):
                file_to_copy = os.path.join(write_from, file)
                shutil.copy(file_to_copy, write_to)
                #print(f"copy {file} from {write_from} to {write_to}")
                logging.info(f'copy "{file}" from "{write_from}"\n          to "{write_to}"')
            else:
                new_dir = os.path.join(write_to, file)
                #print(f"make dir in {write_to} named {file}")
                os.mkdir(new_dir)
                logging.info(f'make dir in "{write_to}" named "{file}"')
                from_next = os.path.join(current_from, file)
                to_next = os.path.join(current_to, file)
                duplicate_files(from_next, to_next)
    except Exception as e:
        logging.error(f'{e}, ending...')
        raise
