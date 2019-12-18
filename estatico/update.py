
import os

from .core import make_post_content, post_preview
from .utils import read_post_with_path, read_blog, blog_paths, content_paths, post_paths
from .setup import ID_MAIN

def update_posts():
    content = [(p,os.path.getmtime(p)) for p in content_paths()]
    posts = [(p,os.path.getmtime(p)) for p in post_paths()]

    return [update_post(post) for post in modified(content, posts)]

def modified(content, posts):
    yield from (p[0] for c,p in zip(content, posts) if c[1] < p[1])

def update_post(post):
    return update_post_teaser(
        *update_post_content(post)
    )

def update_post_content(post):
    return make_post_content(*read_post_with_path(post))

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