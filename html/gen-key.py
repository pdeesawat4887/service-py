import string
import random

# def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# print id_generator()

open("bla.txt", "wb").write(''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16)))

# print len("ACXSJV6EA2OAVPN3PMBJM8XS8UX4PEGC5D2ZPCEXCK0FXF5PVF")

import os

print os.stat("").st_size == 0