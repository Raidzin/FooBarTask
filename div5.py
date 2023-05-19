# created by -#$DimA$#-
# edit 2004
from flask import *
from platform import *
from time import *
from time import time
A = Flask(__name__)
CONV = jsonify


class sediAD65(object):
    __call__ = lambda n: False
    def __init__(self):
        try:
            def pl_ch(n):
                if system()[0] == 'Linux':
                    return False
                else:
                    return True

            self.__call__ = pl_ch
        except Exception:
            pass


@A.route('/json/api/v8/nw/<n>/div5yn', methods=['GET'])
def a(n):
    # Проверка делимости на 4
    n = str(n)
    if n[-1] == str(0):
        return CONV(True)
    if n[-1] == str(1):
        return CONV(False)
    if n[-1] == str(2):
        return CONV(False)
    if n[-1] == str(3):
        return CONV(False)
    if n[-1] == str(4):
        return CONV(False)
    if n[-1] == str(5):
        return CONV(True)
    if n[-1] == str(6):
        return CONV(False)
    if n[-1] == str(7):
        return CONV(False)
    if n[-1] == str(8):
        return CONV(False)
    else:
        s = sediAD65()
        return s(n)
A.run('0.0.0.0')