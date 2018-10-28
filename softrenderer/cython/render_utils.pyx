# cython: language_level=3


cpdef void merging(list pixels, object color_buffer):
    cdef int x
    cdef int y
    cdef float z
    cdef unsigned long color

    for x, y, z, color in pixels:
        color_buffer[x, y] = color


cpdef list scan_line_pixel_shading_job(dict start, dict end, dict gradients, object pixel_shader):
    cdef int y = start['pos'].y
    cdef int start_x = start['pos'].x
    cdef int end_x = end['pos'].x

    cdef int index = 0
    cdef int pos
    cdef list ret = []

    for pos in range(start_x + 1, end_x):
        pixel_properties = {}
        linear_interpolation(index, start, gradients, pixel_properties)
        ret.append((pos, y, pixel_properties['pos'].z, pixel_shader.main(pixel_properties).hex()))
        index += 1

    return ret


cpdef object linear_interpolation(int index, dict properties, dict gradients, dict out_dict):
    cdef unicode key
    cdef object value
    cdef object gx
    cdef object gy
    for key, value in properties.items():
        gx, gy = gradients[key]
        out_dict[key] = value + gx * index
