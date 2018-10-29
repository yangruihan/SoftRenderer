#-*- coding:utf-8 -*-

"""
test performence between list and dict
"""

import timeit
import test_c_dict
import test_c_list

start_v = 0
end_v = 1
t = 0.5

t_list_item = [1.0] * 7
t_list = [t_list_item for _ in range(40000)]

def test_list(start, end, t, t_list):
    for item in t_list:
        for i in item:
            i = start * t + end * (1 - t)

t_dict_item = {
    'pos': [1.0, 1.0, 1.0],
    'color': [1.0, 1.0, 1.0, 1.0]
}
t_dict = [t_dict_item for _ in range(40000)]

def test_dict(start, end, t, t_dict):
    for item in t_dict:
        for k, v in item.items():
            for i in v:
                i = start * t + end * (1 - t)
            
def main():
    t1 = timeit.timeit('test_list(start_v, end_v, t, t_list)', setup='from __main__ import test_list, start_v, end_v, t, t_list', number=1)
    t2 = timeit.timeit('test_dict(start_v, end_v, t, t_dict)', setup='from __main__ import test_dict, start_v, end_v, t, t_dict', number=1)
    t3 = timeit.timeit('test_c_list.test_list(start_v, end_v, t, t_list)', setup='from __main__ import start_v, end_v, t, t_list, test_c_list', number=1)
    t4 = timeit.timeit('test_c_dict.test_dict(start_v, end_v, t, t_dict)', setup='from __main__ import start_v, end_v, t, t_dict, test_c_dict', number=1)

    print('list time cost: %f' % t1)
    print('dict time cost: %f' % t2)
    print('c list time cost: %f' % t3)
    print('c dict time cost: %f' % t4)
    print('-----')
    print('dict time is %fx than list time' % (t2 / t1))
    print('dict time is %fx than c dict time' % (t2 / t4))
    print('dict time is %fx than c list time' % (t2 / t3))
    
if __name__ == '__main__':
    main()
