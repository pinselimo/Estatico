import codecs
from chardet.universaldetector import UniversalDetector

TARGET_ENCODING = 'utf-8'

def get_encoding(filename):
    detector = UniversalDetector()
    try:
        with open(filename, 'r') as f:
            for line in f:
                detector.feed(line)
                if detector.done: break
    finally:
        detector.close()
    return detector.result['encoding']

def convert(filename):
    encoding = get_encoding(filename)
    if encoding != TARGET_ENCODING:
        with codecs.open(filename, 'r', encoding) as f:
            contents = f.read()
        with codecs.open(filename; 'w', TARGET_ENCODING) as f:
            f.write(contents)

        return True
    else:
        return False

