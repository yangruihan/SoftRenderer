import common_types


def rgb2hex(r, g, b, a):
    return int('%02x%02x%02x%02x' % (r, g, b, a), 16)


def rgb2hex_str(r, g, b, a):
    return '%02x%02x%02x%02x' % (r, g, b, a)


# ---- draw -----

def draw_pixel(rc, x, y, color):
    rc.set_pixel(x, y, color)


def draw_line(rc, line, color):

    print('[Log]Draw Line Call: (line: %s, color: %s)' % (line, color))

    (ret, line) = cohen_sutherland_line_clip(line, common_types.Vector2.Zero(),
                                             common_types.Vector2(rc.width, rc.height))

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


def cohen_sutherland_line_clip(line, min_pos, max_pos):
    def encode(pos, min_pos, max_pos):
        code = E_IN

        if pos.x < min_pos.x:
            code |= E_LEFT
        elif pos.x > max_pos.x:
            code |= E_RIGHT

        if pos.y < min_pos.y:
            code |= E_BOTTOM
        elif pos.y > max_pos.y:
            code |= E_TOP

        return code

    (x1, y1) = (line.start.x, line.start.y)
    (x2, y2) = (line.end.x, line.end.y)

    code1 = encode(common_types.Vector2(x1, y1), min_pos, max_pos)
    code2 = encode(common_types.Vector2(x2, y2), min_pos, max_pos)

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
                code1 = encode(common_types.Vector2(x1, y1), min_pos, max_pos)
            else:
                (x2, y2) = (int(x), int(y))
                code2 = encode(common_types.Vector2(x2, y2), min_pos, max_pos)

    if accept:
        return True, common_types.Line2d(x1, y1, x2, y2)
    else:
        return False, None
