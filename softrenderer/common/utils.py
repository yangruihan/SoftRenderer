# -*- coding: utf-8 -*-


def rgb2hex(r, g, b, a):
    try:
        return int('%02x%02x%02x%02x' % (r, g, b, a), 16)
    except Exception:
        print(1)


def rgb2hex_str(r, g, b, a):
    return '%02x%02x%02x%02x' % (r, g, b, a)
