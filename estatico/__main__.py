from .add import add_posts
from .update import update_posts
from .ftp import upload_all

if __name__ == '__main__':
    print('Starting Estatico..')
    added = add_posts()
    print('Pages added: {}'.format(any(added)))
    updated = update_posts()
    print('Updated {} posts'.format(len(list(filter(lambda x:x, updated)))))
    if updated or added:
        print('Uploading...', end=' ')
        try:
            upload_all()
            print('\rUpload successful!')
        except Exception as e:
            print('\rUpload failed with exception: {}'.format(e))
    else:
        print('Nothing to upload.')
