import secrets
import string
import random
import numpy as np
import itertools
from functools import partial
import qrcode

def uidGenerator(_randint=np.random.randint):
        pickchar = partial(secrets.choice, string.ascii_uppercase+string.digits)
        key= ([pickchar() for _ in range(_randint(19, 20))])
        key=''.join(key)
        return key


def image(a):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=6)
    qr.add_data(a)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qr.png','PNG')
