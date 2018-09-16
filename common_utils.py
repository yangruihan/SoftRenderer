def rgb2hex(r, g, b, a):
    return int('%02x%02x%02x%02x' % (r, g, b, a), 16)

def rgb2hex_str(r, g, b, a):
    return '%02x%02x%02x%02x' % (r, g, b, a)

# ---- draw -----

def draw_pixel(rc, x, y, color):
    rc.set_pixel(x, y, color)

def draw_line(rc, x1, y1, x2, y2, color):
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
                    rem -= dx
                    x += 1 if x2 >= x1 else -1
            draw_pixel(rc, x2, y2, color)

