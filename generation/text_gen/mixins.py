import hashlib
from os.path import splitext
from uuid import uuid4


class HexFileName:
    # https: // qna.habr.com / q / 503841
    def get_available_name(name, max_length):
        salt = uuid4().hex
        _, ext = splitext(name)
        # print(_)
        step = max_length - len(_) - len(ext) - 1
        # print(step)


        # print(f'NEW FILENAME:: {str(_ + "_" + str(hashlib.md5(salt.encode() + name.encode()).hexdigest()))[:step] + ext}')
        # print(f'SIZE NEW FILENAME:: {len(str(_ + "_" + str(hashlib.md5(salt.encode() + name.encode()).hexdigest()))[:step] + ext)}')
        return str(_ + "_" + str(hashlib.md5(salt.encode() + name.encode()).hexdigest()))[:step] + ext



'''
The HttpRequest.is_ajax() method is deprecated
'''
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


'''
Handles form error that are passed back to AJAX calls
'''
def FormErrors(*args):
    message = ""
    for f in args:
        if f.errors:
            message = f.errors.as_text()
    return message

