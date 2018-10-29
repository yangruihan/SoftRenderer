cpdef void test_dict(double start, double end, double t, list items):
    cdef dict item
    cdef unicode k
    cdef list v
    cdef double i
    
    for item in items:
        for k, v in item.items():
            for i in v:
                i = start * t + end * (1 - t)