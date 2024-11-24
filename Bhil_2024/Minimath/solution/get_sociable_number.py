import math
import string

#First result: 101916

dvd = {}

def devisors(n):
    '''Generates all devisors of n, except n itself.'''
    assert n < 10_000_000, '' #'Too big number.'

    for i in range(1, n):
        if n % i == 0:
            yield i


def next_number(n):
    '''Returns the sum of all devisors of n.'''
    if n not in dvd.keys():
        dvd[n] = sum(devisors(n))
    return dvd[n]


def get_cycle(n):
    '''
    Generates all numbers in the cycle of n.
    NOTE: Be careful with infinite loops. Use only sociable numbers.
    '''
    c = next_number(n)
    l = 0
    while c != n:
        c = next_number(c)
        yield c
        l += 1
        if l > 100:            
            raise ValueError('Infinite loop detected.')


def scrumble(n):
    n = str(n)

    res = ''
    while len(n) > 4:
        res += n[2:4] + n[0]
        n = n[4:]
    
    return int(res + n)


def main():
    shortest = 1000
    
    for i in range(10_000_000):
        try:
            eq = 'len("' + "a" * i + '")'
            assert set(eq) & set(string.digits) == set(), 'No numbers allowed.'

            n = eval(eq, {name: getattr(math, name) for name in dir(math)})
            res = list(get_cycle(scrumble(n)))
            assert len(res) >= 3, 'Not a sociable number.'        

            print(i)

        except Exception as e:
            pass


if __name__ == '__main__':
    main()