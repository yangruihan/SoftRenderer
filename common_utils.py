# -*- coding: utf-8 -*-


import common_types as ct


def rgb2hex(r, g, b, a):
    return int('%02x%02x%02x%02x' % (r, g, b, a), 16)


def rgb2hex_str(r, g, b, a):
    return '%02x%02x%02x%02x' % (r, g, b, a)


# ---- draw -----

def draw_pixel(rc, x, y, color):
    rc.set_pixel(x, y, color)


def draw_line(rc, line, color):
    print('[Log]Draw Line Call: (line: %s, color: %s)' % (line, color))

    (ret, line) = _cohen_sutherland_line_clip(line, ct.Vector2.zero(),
                                              ct.Vector2(rc.width, rc.height))

    if not ret:
        print('[Log]Line was aborted')
        return
    else:
        print('[Log]Will draw line %s' % line)

    (x1, y1) = (line.start.x, line.start.y)
    (x2, y2) = (line.end.x, line.end.y)

    # draw a pixel
    if x1 == x2 and y1 == y2:
        draw_pixel(rc, x1, y1, color)
    # draw a vertical line
    elif x1 == x2:
        inc = 1 if y1 <= y2 else -1
        for y in range(y1, y2 + inc, inc):
            draw_pixel(rc, x1, y, color)
    # draw a horizontal line
    elif y1 == y2:
        inc = 1 if x1 <= x2 else -1
        for x in range(x1, x2 + inc, inc):
            draw_pixel(rc, x, y1, color)
    else:
        dx = x2 - x1 if x1 < x2 else x1 - x2
        dy = y2 - y1 if y1 < y2 else y1 - y2

        if dx >= dy:
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            y = y1
            rem = 0
            for x in range(x1, x2 + 1):
                draw_pixel(rc, x, y, color)
                rem += dy
                if rem >= dx:
                    rem -= dx
                    y += 1 if y2 >= y1 else -1
            draw_pixel(rc, x2, y2, color)
        else:
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            x = x1
            rem = 0
            for y in range(y1, y2 + 1):
                draw_pixel(rc, x, y, color)
                rem += dx
                if rem >= dy:
                    rem -= dy
                    x += 1 if x2 >= x1 else -1
            draw_pixel(rc, x2, y2, color)


E_LEFT = 1
E_TOP = 1 << 1
E_RIGHT = 1 << 2
E_BOTTOM = 1 << 3
E_IN = 0


def _cohen_sutherland_line_clip(line, min_pos, max_pos):
    def encode(pos, _min_pos, _max_pos):
        _code = E_IN

        if pos.x < _min_pos.x:
            _code |= E_LEFT
        elif pos.x > _max_pos.x:
            _code |= E_RIGHT

        if pos.y < _min_pos.y:
            _code |= E_BOTTOM
        elif pos.y > _max_pos.y:
            _code |= E_TOP

        return _code

    (x1, y1) = (line.start.x, line.start.y)
    (x2, y2) = (line.end.x, line.end.y)

    code1 = encode(ct.Vector2(x1, y1), min_pos, max_pos)
    code2 = encode(ct.Vector2(x2, y2), min_pos, max_pos)

    accept = False

    while True:
        if code1 | code2 == 0:
            accept = True
            break

        elif code1 & code2 != 0:
            break

        else:
            code = code1 if code1 != 0 else code2
            (x, y) = (0, 0)
            if code & E_TOP != 0:
                x = x1 + (x2 - x1) * (max_pos.y - y1) / (y2 - y1)
                y = max_pos.y
            elif code & E_BOTTOM != 0:
                x = x1 + (x2 - x1) * (min_pos.y - y1) / (y2 - y1)
                y = min_pos.y
            elif code & E_LEFT != 0:
                x = min_pos.x
                y = y1 + (y2 - y1) * (min_pos.x - x1) / (x2 - x1)
            elif code & E_RIGHT != 0:
                x = max_pos.x
                y = y1 + (y2 - y1) * (max_pos.x - x1) / (x2 - x1)

            if code == code1:
                (x1, y1) = (int(x), int(y))
                code1 = encode(ct.Vector2(x1, y1), min_pos, max_pos)
            else:
                (x2, y2) = (int(x), int(y))
                code2 = encode(ct.Vector2(x2, y2), min_pos, max_pos)

    if accept:
        return True, ct.Line2d(x1, y1, x2, y2)
    else:
        return False, None


def draw_triangle(rc, v1, v2, v3, color):
    # sort three vertices by y-coordinate
    (v1, v2, v3) = sorted([v1, v2, v3], key=lambda v: v.y)

    if v2.y == v3.y:
        _fill_top_flat_triangle(rc, v1, v2, v3, color)
    elif v2.y == v1.y:
        _fill_bottom_flat_triangle(rc, v3, v1, v2, color)
    else:
        v4 = ct.Vector2(int(v1.x + (v2.y - v1.y) * (v3.x - v1.x) / (v3.y - v1.y)), v2.y)
        _fill_top_flat_triangle(rc, v1, v2, v4, color)
        _fill_bottom_flat_triangle(rc, v3, v2, v4, color)


def _fill_bottom_flat_triangle(rc, v1, v2, v3, color):
    inv_slope1 = (v2.x - v1.x) / (v2.y - v1.y)
    inv_slope2 = (v3.x - v1.x) / (v3.y - v1.y)

    (cx1, cx2) = (v1.x, v1.x)

    for y in range(v1.y, v2.y - 1, -1):
        draw_line(rc, ct.Line2d(int(cx1), y, int(cx2), y), color)
        cx1 += inv_slope1
        cx2 += inv_slope2


def _fill_top_flat_triangle(rc, v1, v2, v3, color):
    inv_slope1 = (v2.x - v1.x) / (v2.y - v1.y)
    inv_slope2 = (v3.x - v1.x) / (v3.y - v1.y)

    (cx1, cx2) = (v1.x, v1.x)

    for y in range(v1.y, v2.y + 1):
        draw_line(rc, ct.Line2d(int(cx1), y, int(cx2), y), color)
        cx1 += inv_slope1
        cx2 += inv_slope2
