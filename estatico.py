import os
from bs4 import BeautifulSoup
from markdown import markdown
from functools import reduce

STATIC_FOLDER = 'blog'
POST_FOLDER = 'posts'
TEMPLATE_FOLDER_ABSOLUTE = os.path.join(STATIC_FOLDER,'templates')
CONTENT_FOLDER = 'content'
CONTENT_FOLDER_ABSOLUTE = os.path.join(STATIC_FOLDER, CONTENT_FOLDER)
IMAGE_PATH = 'images'
IMAGE_PATH_ABSOLUTE = os.path.join(CONTENT_FOLDER_ABSOLUTE, IMAGE_PATH)
IMAGE_SIZE = '500px'
HTML = '.html'
POST_FORMATS = ['.md','.html']
PAGE_NAME = 'blog_{}.html'
CONT_NAME = '{}.html'
TEMPLATE = os.path.join(TEMPLATE_FOLDER_ABSOLUTE, PAGE_NAME.format('template'))
POST_TEMPLATE = os.path.join(TEMPLATE_FOLDER_ABSOLUTE, CONT_NAME.format('post_template'))
POST_PREVIEW_TEMPLATE = '<p><h3><a href={}>{}</a></h3>{}'
ID_BLOG_LINKS = {id:'bloglinks'}
LIMIT = 10
ID_MAIN = {'id':'main'}
H3 = 'h3'
MORE =  'More..'

def main():
    add_posts()
    update_posts()

def add_posts():
    content = content_paths()
    posts = post_paths()

    added = (add_post(post) for post in new_content(content, posts))
    print("New Pages: {}".format(any(added)))

def update_posts():
    content = [(p,os.path.getmtime(p)) for p in content_paths()]
    posts = [(p,os.path.getmtime(p)) for p in post_paths()]

    updated = (update_post(post) for post in modified(content, posts))
    print("Updated Posts: {}".format(any(updated)))

def blog_paths():
    return [
        os.path.join(STATIC_FOLDER,file)
        for file in sortedbycdate(STATIC_FOLDER, os.listdir(STATIC_FOLDER))
        if file.endswith(HTML)
        ]

def post_paths():
    return [
        os.path.join(POST_FOLDER,file)
        for file in sortedbycdate(POST_FOLDER, os.listdir(POST_FOLDER))
        if any(file.endswith(end) for end in POST_FORMATS)
        ]

def content_paths():
    return [
        os.path.join(CONTENT_FOLDER_ABSOLUTE,file)
        for file in sortedbycdate(CONTENT_FOLDER_ABSOLUTE, os.listdir(CONTENT_FOLDER_ABSOLUTE))
        if file.endswith(HTML)
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
    return ('.'.join(os.path.split(filepath)[-1].split('.')[:-1]+['html']), read_post(filepath))

def new_content(content, posts):
    cs = {os.path.split(c)[-1].split('.')[-2] for c in content}
    yield from (p for p in posts if os.path.split(p)[-1].split('.')[-2] not in cs)

def modified(content, posts):
    yield from (p[0] for c,p in zip(content, posts) if c[1] < p[1])

def update_post(post):
    return update_post_teaser(
        *update_post_content(post)
    )

def update_post_content(post):
    return add_post_content(*read_post_with_path(post))

def update_post_teaser(link, title, teaser):
    for filepath in blog_paths(): 
        soup = read_blog(filepath)
        for post in soup.find(**ID_MAIN).div.find_all('p'):
            if not post.h3:
                continue
            if link in post.h3.a['href'] or title in post.h3.get_text():
                post.replaceWith(post_preview(link, title, teaser))
                with open(filepath, 'w') as f:
                    f.write(str(soup.prettify()))
                return True
    else:
        return False

def add_post(post):
    return add_post_link(
        add_post_content(*read_post_with_path(post))
    )

def dissect(post):
    return (
        post.a['href'],
        post.h3.get_text(), 
        '<br>'.join(post.get_text().splitlines()[1:])
    )

def add_post_content(filename, post_soup):
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

def add_post_link(post):
    def inner(post, content):
        soup,*rest = content
        post_tag = post_preview(*post)

        soup.find(**ID_MAIN).div.header.insert_after(post_tag)

        all_posts = soup.find(**ID_MAIN).div.find_all('p')
        if len(all_posts) > LIMIT + 1:
            post_mv = dissect(all_posts[-1])
            all_posts[-1].decompose()
            return inner(post_mv, new_page(rest)) + [soup]
        else:
            return [soup]

    curr = get_blogs()
    soups = inner(post, new_page(curr))
    for i in range(len(soups)):
        soup = soups.pop()
        if len(soups): # link next page
            soup.find(*ID_BLOG_LINKS).a['href'] = PAGE_NAME.format(i+1)
            soup.find(*ID_BLOG_LINKS).a.string = MORE
        with open(os.path.join(STATIC_FOLDER,PAGE_NAME.format(i)),'w') as f:
            f.write(str(soup.prettify()))

    return i > len(curr) # New pages added?

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

def sortedbycdate(folder, files):
    return sorted(files, key=lambda f: os.path.getctime(os.path.join(folder,f)))

def sortedbymdate(folder, files):
    return sorted(files, key=lambda f: os.path.getmtime(os.path.join(folder,f)))

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

if __name__ == '__main__':
    main()