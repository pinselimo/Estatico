from ftplib import FTP_TLS
from ssl import create_default_context
from contextlib import contextmanager
import os

from .setup import SERVERNAME, USERNAME, PASSWD, BLOG_SERVERSIDE_DIRECTORY
from .utils import blog_paths, content_paths, image_paths

def upload_all():
    with ftps_client() as ftps:
        upload_blogs(ftps)
        upload_contents(ftps)
        upload_images(ftps)

def upload_files(filenames):
    with ftps_client() as ftps:
        for filename in filenames:
            upload(ftps, filename)

@contextmanager
def ftps_client():
    ftps = FTP_TLS(host=SERVERNAME, user=USERNAME, passwd=PASSWD, context=create_default_context())
    ftps.prot_p()
    ftps.cwd(BLOG_SERVERSIDE_DIRECTORY)
    try:
        yield ftps
    finally:
        ftps.quit()

def upload(ftps, filename):
    filename = '/'.join(os.path.split(filename))
    with open(filename,'rb') as fp:
        ftps.storbinary(cmd="STOR {}".format(filename), fp=fp)

def upload_blogs(ftps):
    for blog in blog_paths():
        upload(ftps, blog)

def upload_contents(ftps):
    for cont in content_paths():
        upload(ftps, cont)

def upload_images(ftps):
    for img in image_paths():
        upload(ftps, img)