cpdef void test_list(double start, double end, double t, list items):
    cdef list item
    cdef double i

    for item in items:
        for i in item:
            i = start * t + end * (1 -t)