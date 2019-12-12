import os
from bs4 import BeautifulSoup

from .utils import blog_paths
from .setup import POST_TEMPLATE, CONTENT_FOLDER, IMAGE_PATH, IMAGE_SIZE, IMAGE_PATH_ABSOLUTE, \
    ID_MAIN, STATIC_FOLDER, PAGE_NAME, TEMPLATE, POST_PREVIEW_TEMPLATE

def make_post_content(filename, post_soup):
    with open(POST_TEMPLATE,'r') as temp:
        soup = BeautifulSoup(temp.read(),features='html.parser')

    title = post_soup.h1.text
    subtitle = post_soup.h2.text
    teaser = post_soup.p.text
    filepath = os.path.join(CONTENT_FOLDER, filename)

    for img in post_soup.find_all('img'):
        img['width'] = IMAGE_SIZE
        name = IMAGE_PATH + '/' + img['src'].split('/')[-1]
        img['src'] = name
        if name.split('/')[-1] not in os.listdir(IMAGE_PATH_ABSOLUTE):
            print('Attention: Image {} not found!'.format(name))

    soup.find(**ID_MAIN).div.header.h1.string = title
    soup.find(**ID_MAIN).div.header.p.string = subtitle
    post_soup.h1.decompose()
    post_soup.h2.decompose()
    soup.find(**ID_MAIN).div.header.insert_after(post_soup)
    
    with open(os.path.join(STATIC_FOLDER, filepath),'w') as f:
        f.write(str(soup.prettify()))

    return CONTENT_FOLDER + '/' + filename, title, teaser

def new_page(rest):
    if not len(rest):
        with open(TEMPLATE,'r') as temp:
            soup = BeautifulSoup(temp.read(),features='html.parser')
        with open(os.path.join(STATIC_FOLDER,PAGE_NAME.format(len(blog_paths()))),'w') as f:
            f.write(str(soup.prettify()))
        return [soup]
    else:
        return rest

def post_preview(link, title, teaser):
    return BeautifulSoup(POST_PREVIEW_TEMPLATE.format(link, title, teaser),features='html.parser')
