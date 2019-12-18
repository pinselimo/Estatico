import os

from .core import make_post_content, post_preview, new_page
from .utils import dissect, get_blogs, read_post_with_path, content_paths, post_paths
from .setup import ID_MAIN, STATIC_FOLDER, LIMIT, ID_BLOG_LINKS, MORE, PAGE_NAME

def add_posts():
    content = content_paths()
    posts = post_paths()

    return [add_post(post) for post in new_content(content, posts)]
    
def new_content(content, posts):
    cs = {os.path.split(c)[-1].split('.')[-2] for c in content}
    yield from (p for p in posts if os.path.split(p)[-1].split('.')[-2] not in cs)

def add_post(post):
    return add_post_link(
        add_post_content(post)
    )

def add_post_content(post):
    return make_post_content(*read_post_with_path(post))

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

    return i+1 > len(curr) # New pages added?