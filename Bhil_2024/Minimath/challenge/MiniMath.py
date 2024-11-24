import math
import string

def devisors(n):
    '''Generates all devisors of n, except n itself.'''
    assert n < 10_000_000, 'Too big number.'

    for i in range(1, n):
        if n % i == 0:
            yield i


def next_number(n):
    '''Returns the sum of all devisors of n.'''
    return sum(devisors(n))


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
    while True:
        try:
            eq = input('Please enter an equation: ')
            assert set(eq) & set(string.digits) == set(), 'No numbers allowed.'

            n = eval(eq, {name: getattr(math, name) for name in dir(math)})
            #print(f'{n=}')
            #print(f'{scrumble(n)=}')
            res = list(get_cycle(scrumble(n)))
            #print(f'{res=}')
            assert len(res) >= 3, 'Not a sociable number.'

            print('Length:', len(eq))
            if len(eq) < shortest:
                shortest = len(eq)
                print('New Best!')
            else:
                print('Can you make it a bit shorter please?')
                print('Best so far:', shortest)
        except Exception as e:
            # print the exception and continue
            print(e)


if __name__ == '__main__':
    main()