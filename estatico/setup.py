import os

STATIC_FOLDER = 'blog'
POST_FOLDER = 'posts'
TEMPLATE_FOLDER_ABSOLUTE = os.path.join(STATIC_FOLDER,'templates')
CONTENT_FOLDER = 'content'
CONTENT_FOLDER_ABSOLUTE = os.path.join(STATIC_FOLDER, CONTENT_FOLDER)
IMAGE_PATH = 'images'
IMAGE_PATH_ABSOLUTE = os.path.join(CONTENT_FOLDER_ABSOLUTE, IMAGE_PATH)
IMAGE_SIZE = '500px'
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