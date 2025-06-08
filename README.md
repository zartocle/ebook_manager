### Ebook manager


This is a little educational project I'm using to learn Python; a program that, once given a directory path, will scan all files contained in it and, for those that are found to be ebooks, will parse file metadata and rename the file accordingly, based on the structure _<book_name>\_<author_name>_



It was developed using a virtual environment created with the `venv` package and is provided with a `requirements.txt` file that provides the list of python packages that are necessary to its execution


#### How to prepare the environment to execute the program (currently works on Ubuntu Linux only):

1. (Recommended:) Create a virtual environment with the tool of your choice

    `python3 -m venv <env_name>`

    Activate the virtual environment:
    `source <env_name>/bin/activate`

    > To deactivate the virtual environment:    `deactivate`

2. Install the following packages: 

        * `libdjvulibre-dev`, `pkg-config` (for support to DJVU files)
        * `libcairo2-dev`, `gobject-introspection` (for support to python bindings for GNOME)


3. Install the packages listed in `requirements.txt` with:

    `python -m pip install -r path/to/requirements.txt`   

    >
    >How to automatically generate a `requirements.txt` file:
    >
    >    `pip install pipreqs
    > pipreqs /path/to/project`


<br><br><br><br><br><br>


[Markdown syntax reference guide](https://www.markdownguide.org/basic-syntax/)

[Markdown editor to test your syntax](https://stackedit.io/app#)
