import os
from bs4 import BeautifulSoup
from markdown import markdown

from .setup import STATIC_FOLDER, STATIC_FOLDER, POST_FOLDER, CONTENT_FOLDER_ABSOLUTE, \
    POST_FORMATS, CONT_NAME, IMAGE_PATH_ABSOLUTE, IMAGE_FORMATS

HTML = '.html'

def dissect(post):
    return (
        post.a['href'],
        post.h3.get_text(), 
        '<br>'.join(post.get_text().splitlines()[1:])
    )

def blog_paths():
    return [
        os.path.join(STATIC_FOLDER,file)
        for file in sortedbycdate(STATIC_FOLDER, os.listdir(STATIC_FOLDER))
        if file.lower().endswith(HTML)
        ]

def post_paths():
    return [
        os.path.join(POST_FOLDER,file)
        for file in sortedbycdate(POST_FOLDER, os.listdir(POST_FOLDER))
        if any(file.lower().endswith(end) for end in POST_FORMATS)
        and not file.startswith('_')
        ]

def content_paths():
    return [
        os.path.join(CONTENT_FOLDER_ABSOLUTE,file)
        for file in sortedbycdate(CONTENT_FOLDER_ABSOLUTE, os.listdir(CONTENT_FOLDER_ABSOLUTE))
        if file.lower().endswith(HTML)
        ]

def image_paths():
    return [
        os.path.join(IMAGE_PATH_ABSOLUTE, file)
        for file in sortedbycdate(IMAGE_PATH_ABSOLUTE, os.listdir(IMAGE_PATH_ABSOLUTE))
        if any(file.lower().endswith(end) for end in IMAGE_FORMATS)
        ]

def get_blogs():
    return [read_blog(fp) for fp in blog_paths()]

def get_posts():
    return [read_post(fp) for fp in post_paths()]
   
def read_blog(filepath):
    with open(filepath,'r') as f:
        return BeautifulSoup(f.read(), features='html.parser')

def read_post(filepath):
    with open(filepath,'r') as f:
        return BeautifulSoup(
            markdown(f.read(),extensions=['fenced_code']), 
            features='html.parser'
            )

def read_post_with_path(filepath):
    filename = '.'.join(os.path.split(filepath)[-1].split('.')[:-1])
    return (CONT_NAME.format(filename), read_post(filepath))

def sortedbycdate(folder, files):
    return sorted(files, key=lambda f: os.path.getctime(os.path.join(folder,f)))

# unused / unnecessary - names are now copied. Maybe useful for blog page naming?
def check_exist(filepath):
    absolute_filepath = os.path.join(STATIC_FOLDER,filepath)
    if os.path.exists(absolute_filepath):
        spl = filepath.split('.')
        name = spl[-2]
        try:
            num = int(name.split('_')[-1])
            num += 1
        except ValueError:
            with open(absolute_filepath, 'r') as f:
                content = f.read()
            os.unlink(absolute_filepath)
            with open(os.path.join(STATIC_FOLDER,'.'.join(spl[:-2]+[name+'_0',spl[-1]])), 'w') as f:
                f.write(content)
            num = 1
        return '.'.join(spl[:-2]+[name+'_%i'%num,spl[-1]])
    else:
        return filepath