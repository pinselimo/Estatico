from configparser import ConfigParser, ExtendedInterpolation

SETUP = 'setup.cfg'

config = ConfigParser(interpolation=ExtendedInterpolation(), delimiters=('=',), comment_prefixes=(';',), inline_comment_prefixes=())
config.read(SETUP)

template = config['template']
STATIC_FOLDER = template['STATIC_FOLDER']
POST_FOLDER = template['POST_FOLDER']
TEMPLATE_FOLDER_ABSOLUTE = template['TEMPLATE_FOLDER_ABSOLUTE']
CONTENT_FOLDER = template['CONTENT_FOLDER']
CONTENT_FOLDER_ABSOLUTE = template['CONTENT_FOLDER_ABSOLUTE']
IMAGE_PATH = template['IMAGE_PATH']
IMAGE_PATH_ABSOLUTE = template['IMAGE_PATH_ABSOLUTE']
IMAGE_SIZE = template['IMAGE_SIZE']
IMAGE_FORMATS = list(template['IMAGE_FORMATS'].split(','))
POST_FORMATS = list(template['POST_FORMATS'].split(','))
PAGE_NAME = template['PAGE_NAME']
CONT_NAME = template['CONT_NAME']
TEMPLATE = template['PAGE_TEMPLATE_NAME']
POST_TEMPLATE = template['POST_TEMPLATE_NAME']
POST_PREVIEW_TEMPLATE = template['POST_PREVIEW_TEMPLATE']
ID_BLOG_LINKS = {'id':template['ID_BLOG_LINKS']}
LIMIT = int(template['LIMIT'])
ID_MAIN = {'id':template['ID_BLOGENTRY']}
H3 = template['TAG_HEADING']
MORE =  template['MORE']

server = config['server']
SERVERNAME = server['SERVERNAME']
USERNAME = server['USERNAME']
PASSWD = server['PASSWD']
BLOG_SERVERSIDE_DIRECTORY = server['BLOG_SERVERSIDE_DIRECTORY']