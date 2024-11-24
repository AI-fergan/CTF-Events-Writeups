import math

#First result: 101916

LEN_LINE = 'len("%s")'
POW_LINE = 'pow(%s,%s)'
BASE = 4

def getn(n = 4):
    """
    This function return numbers string by using 'len()' func.
    """
    return (LEN_LINE % ("a" * n))

def getp(a,b):
    """
    This function return numbers string by using 'pow()' func.
    """
    return(POW_LINE % (getn(a),getn(b)))

def getans(num, calc_method):
    """
    This function get the calc method and the number that the user
    want to calc, then it will get the dummy numbers (not real numbers, the numbers is functions output)
    and return python line that calc the user input number.
    """
    res = ""

    # Run until the line can calc all the user number
    while num != 0:
        # Add new part for the calc line
        out = calc_method(num)
        num = out[1]        

        # Check if the line is already fill with something or not
        if len(res):
            res += "+" + out[0]
        else:
            res = out[0]
        
    return res


def calc_using_len(n):
    """
    This function return python line code with 'len()' functions that return number.
    """
    crr = 1
    res = ""
    if n <= 4: # Check if the number is too small
        return (getn(n), 0)
    
    # Create python line using 'len()' functions to calc the number
    while n >= crr * 4:
        crr *= 4
        res += getn() + "*"

    # Remove the last '*' sign
    res = res[:-1]

    # Return tuple of the python line and the rest of the number
    return (res, n - crr)

def calc_using_pow(n):
    """
    This function return python line code with 'len()' functions that return number.
    """
        
    res = ""

    if n <= 4: # Check if the number is too small
        return (getn(n), 0)
    
    ans = int(math.log(n,BASE)) # Get the base number for the pow action

    res = getp(BASE, ans) # Get pow python line string

    # Return the python line and the rest of the number
    return (res, n - pow(BASE, ans))


def main():
    num = int(input("num: ")) # User input number

    # Init the pow calc method by default
    calc_method = calc_using_pow

    # Default number
    if num == 0:
        num = 101916

    # Get user option for Calc method
    op = input("1. calc using len\n2. calc using pow\noption: ")
    if op == "1":
        calc_method = calc_using_len

    # Get output of python calc line for the user number
    res = getans(num, calc_method)

    # Profit
    print("int(" + res + ")")

if __name__ == "__main__":
    main()