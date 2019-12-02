import os
from bs4 import BeautifulSoup
from markdown import markdown
from functools import reduce

STATIC_FOLDER = "blog"
CONTENT_FOLDER = "posts"
TEMPLATE_FOLDER = STATIC_FOLDER + '/' + "templates"
POST_FOLDER = STATIC_FOLDER + '/' + CONTENT_FOLDER
IMAGE_PATH = "images"
IMAGE_PATH_ABSOLUT = POST_FOLDER + '/' + IMAGE_PATH
HTML = ".html"
MD = ".md"
PAGE_NAME = "blog_{}.html"
CONT_NAME = "{}.html"
TEMPLATE = TEMPLATE_FOLDER + '/' + PAGE_NAME.format("template")
POST_TEMPLATE = TEMPLATE_FOLDER + '/' + CONT_NAME.format("post_template")
BLOG_LINKS = "bloglinks"
LIMIT = 10

def main():
    pages = get_current()
    posts = get_posts()
    for post in new_content(pages, posts):
        add_post(post)

def get_current():
    pages = []
    for file in os.listdir(STATIC_FOLDER):
        if file.endswith(HTML):
            with open(STATIC_FOLDER + '/' + file,'r') as f:
                pages.append(f.read())
    return pages

def get_posts():
    posts = []
    for file in os.listdir(CONTENT_FOLDER):
        if file.endswith(MD) or file.endswith(HTML):
            with open(CONTENT_FOLDER + '/' + file,'r') as f:
                posts.append(markdown(f.read()))
    return posts
    
def new_content(pages, content):
    headings = map(lambda s: s.lower(), reduce(lambda a,b: a+b, [
        BeautifulSoup(page,features="html.parser").find(id="main").div.find_all('h3') 
        for page in pages
        ]))
        
    return [
        cont
        for cont in content
        for title in (BeautifulSoup(cont,features="html.parser").h1.get_text().lower().strip(),)
        if title not in headings
    ]

def add_post(post):
    return add_post_link(
        add_post_content(post)
    )

def dissect(post):
    return (
        post.a['href'],
        post.h3.get_text(), 
        "<br>".join(post.get_text().splitlines()[1:])
    )

def add_post_content(post):
    with open(POST_TEMPLATE,'r') as temp:
        soup = BeautifulSoup(temp.read(),features="html.parser")

    post_soup = BeautifulSoup(post,features="html.parser")
    title = post_soup.h1.text
    subtitle = post_soup.h2.text
    teaser = post_soup.p.text
    filename = CONT_NAME.format('_'.join(title.split(' ')).lower())
    address = CONTENT_FOLDER + "/" + filename

    for img in post_soup.find_all("img"):
        name = img['src']
        if IMAGE_PATH not in name[:name.find('/')]:
            name = IMAGE_PATH + "/" + img['src']
            img['src'] = name
        if not name[name.rfind('/')+1:] in os.listdir(IMAGE_PATH_ABSOLUT):
            print("Attention: Image {} not found!".format(name))

    soup.find(id="main").div.header.h1.string = title
    soup.find(id="main").div.header.p.string = subtitle
    post_soup.h1.decompose()
    post_soup.h2.decompose()
    soup.find(id="main").div.header.insert_after(post_soup)
    
    with open(STATIC_FOLDER + "/" + address,'w') as f:
        f.write(str(soup.prettify()))

    return address, title, teaser

def add_post_link(post):
    def inner(post, content):
        c,*rest = content
        post_tag = BeautifulSoup("<p><h3><a href={}>{}</a></h3>{}".format(*post),features="html.parser")

        soup = BeautifulSoup(c,features="html.parser")
        soup.find(id="main").div.header.insert_after(post_tag)

        all_posts = soup.find(id="main").div.find_all('p')
        if len(all_posts) > LIMIT + 1:
            return inner(dissect(all_posts[-1]), new_page(rest)).append(soup)
        else:
            return [soup]

    curr = get_current()
    soups = inner(post, curr)
    for i in range(len(soups)):
        s = soups.pop()
        if len(soups): # link next page
            s.find(id=BLOG_LINKS).a['href'] = PAGE_NAME.format(i+1)
            s.find(id=BLOG_LINKS).a.string = "More.."
        with open(STATIC_FOLDER+'/'+PAGE_NAME.format(i),'w') as f:
            f.write(str(s.prettify()))

    return i > len(curr) # New pages added?

def new_page(rest):
    if not len(rest):
        with open(TEMPLATE,'r') as temp:
            soup = BeautifulSoup(temp.read(),features="html.parser")
        with open(STATIC_FOLDER + '/' + PAGE_NAME.format(len(get_current())),'w') as f:
            f.write(str(soup))
        return [str(soup)]
    else:
        return rest

if __name__ == "__main__":
    main()