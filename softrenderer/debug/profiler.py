# -*- coding:utf-8 -*-


import time


class Profiler:
    class Data:
        def __init__(self, event_name):
            self.event_name = event_name
            self.start_time = None
            self.end_time = None
            self.duration = None
            self.times = 0

        def start(self):
            self.start_time = time.clock() * 1000
            self.times += 1
            return self.start_time

        def end(self):
            self.end_time = time.clock() * 1000
            self.duration = self.end_time - self.start_time
            return self.duration

        def clear(self):
            self.times = 0

    ENABLE = 0
    DISABLE = 1

    _instance = None
    _enable = True

    def __init__(self):
        self._data = {}
        self._event_stack = []
        self._before_update_time = None
        self._after_update_time = None

    def _push_event(self, event_name):
        self._event_stack.append(event_name)

        if event_name in self._data:
            self._data[event_name].start()
        else:
            data = Profiler.Data(event_name)
            data.start()
            self._data[event_name] = data

    def _pop_event(self):
        event_name = self._event_stack.pop()
        self._data[event_name].end()

    def _clear(self):
        for v in self._data.values():
            v.clear()

    @classmethod
    def config(cls, enable):
        cls._enable = enable == cls.ENABLE

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Profiler()

        return cls._instance

    @classmethod
    def begin(cls, event_name):
        if not cls._enable:
            return

        cls.instance()._push_event(event_name)

    @classmethod
    def end(cls):
        if not cls._enable:
            return

        cls.instance()._pop_event()

    @classmethod
    def before_update(cls):
        if not cls._enable:
            return

        cls.instance()._before_update_time = time.clock() * 1000

    @classmethod
    def after_update(cls):
        if not cls._enable:
            return
        cls.instance()._after_update_time = time.clock() * 1000

        cls._statistics()

        cls.instance()._clear()

    @classmethod
    def _statistics(cls):
        if not cls._enable:
            return

        print('\n----- Profiler Statistics -----')
        ins = cls.instance()
        sum_time = ins._after_update_time - ins._before_update_time
        print('* Delta time: %fms -- FPS: %f\n-' % (sum_time, 1000 / sum_time))
        for k, v in ins._data.items():
            module_level = len(k.split('.')) - 1
            indent = "\t" * module_level
            print('- %s%s: | Percent %.2f%% | Duration %fms | Times: %d' % (
                indent,
                k,
                v.duration * v.times * 100 / sum_time,
                v.duration,
                v.times))
        print('-\n-------------------------------')
