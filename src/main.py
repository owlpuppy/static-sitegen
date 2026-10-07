# static-sitegen main

from generate_pages import generate_page
from file_operations import duplicate_files

def main():
    duplicate_files()
    generate_page('index.md', 'template.html')
    generate_page('blog/glorfindel/index.md', 'template.html', 'blog/glorfindel')
    generate_page('blog/majesty/index.md', 'template.html', 'blog/majesty')
    generate_page('blog/tom/index.md', 'template.html', 'blog/tom')
    generate_page('contact/index.md', 'template.html', 'contact')




if __name__ == "__main__":
    main()
