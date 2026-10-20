# static-sitegen  
** generate static HTML website using provided files and template **

This was originally a Boot.dev project, I have made a few modifications.

## Purpose  
Generate static HTML website by copying static files to destination location, and then generate pages from source markdown documents using a template file.

## Use  
navigate to directory with build.sh and main.sh (scripts must be made executable)

### generate site using optional basepath
```./build.sh```

### generate site for local testing in "public" (localhost:8888)
```./main.sh```

### run unit tests
```./test.sh```

Shell scripts can be edited to suit the desired outcomes. 

## Completed modifications  
- added HTMLNode class attribute “no_close”, boolean flag to identify self closing HTML tags, defaults to false, currently used for "img" tags
- added automatic selection of delimiter by TextType in split_nodes_delimiter
- added html.escape to extract_title and text_to_textnode
- added argument parsing
    - added verbose if argument provided, can override and print to terminal
    - added build argument with optional basepath, defaults to “/”
- added logging
- added automatic creation of public and docs destinations if they are missing
- added basic escape for urls in textnode
- changed "b" and "i" tags to "strong" and "em"

## Possible  
- add filecounts
- add elapsed time 
- add verification of internal links (possible optional verification step)
- add nested tag parsing

Last updated: 20 October 2026
