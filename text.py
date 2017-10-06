from multiprocessing import Pool
import itertools

def f(x,y,z):
    return x+y+z

def f_helper(x):
    return f(x[0],x[1],x[2])

if __name__ == '__main__':
    p = Pool(4)
    arg_list=[['a', 'b', 'd'], ['c', 'd', 'f'], ['e', 'f', 'f']]
    print p.map(f_helper, arg_list)
