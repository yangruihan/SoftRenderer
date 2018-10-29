# cython: language_level=3


cpdef void merging(list pixels, object color_buffer):
    cdef int x
    cdef int y
    cdef double z
    cdef unsigned long color

    for x, y, z, color in pixels:
        color_buffer[x, y] = color


cpdef list scan_line_pixel_shading_job(list start, int end_x, list gradients, object pixel_shader):
    cdef int start_x = start[0]
    cdef int y = start[1]

    cdef int index = 0
    cdef int x
    cdef list ret = []
    cdef list pixel_properties

    cdef int i
    cdef int properties_len = len(start)
    cdef double gx
    cdef double gy

    for x in range(start_x + 1, end_x):
        pixel_properties = [x, y]

        for i in range(2, properties_len):
            gx, gy = gradients[i]
            pixel_properties.append(start[i] + gx * index)

        ret.append((x, y, pixel_properties[2], pixel_shader.main(pixel_properties).hex()))
        index += 1

    return ret
