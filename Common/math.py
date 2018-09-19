class Vector2:
    _Zero = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector2(%s, %s)' % (self.x, self.y)

    @classmethod
    def zero(cls):
        if cls._Zero is None:
            cls._Zero = Vector2(0, 0)
        return cls._Zero
