# src/generate_pages.py

def extract_title(markdown: str) -> str:
    header = None
    for line in markdown:
        if line.startswith('# '):
            header = line[2:].strip()

    if header is None:
        raise ValueError("top level header is missing from markdown")
    return header
